## API setup/guide instructions

Run the following commands to get started:
```
sh ./install.sh
sh ./run.sh
```
## GET /api/polls/
Get a list of available polls 
* ### Response 200

```
[
    {
        "id": 1,
        "name": "Poll #1",
        "start_date": "2021-03-17T00:00:00+03:00",
        "finish_date": "2021-03-19T00:00:00+03:00",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis sed."
    },
    ...
]
```
## GET /api/polls/\<int:pk>/
Get a list of the chosen poll
+ ### URL parameters
    + `<int:pk>` - id of a poll
* ### Response 200

```
[
    {
        "id": 2,
        "question_text": "Nam blandit enim vel finibus commodo.",
        "choices": "Cras pellentesque eros non mattis ultrices,\r\nFusce vitae enim ut magna tempor dapibus eu nec arcu,\r\nCras in magna at velit hendrerit ornare",
        "question_type": "select",
        "created": "2021-03-17T15:42:54.329169+03:00",
        "poll": 1
    },
    ...
]
```
## POST /api/polls/\<int:pk>/
Send your answers to questions

+ ### URL parameters
    + `<int:pk>` - id of a poll
+ ### Request
```
/api/polls/1/
```
+ ### Body
```
{
    "user_id": 1,
    "answers": [
        {"question": 2, "answer_text": "Fusce vitae"},
        {"question": 3, "answer_text": "Morbi a justo erat, Nunc faucibus enterdum"},
        {"question": 4, "answer_text": "Justo consectetur ullamcorper nec accumsan erat"}
    ],
    "is_anonymous": true
}
```
* Description:
    + value of `"user_id"` - id of the user
    + value of `"question"` - id of the question
    + value of `"answer_text"` - your answer
    + if value of `"question_type"` - `"select"`, your answer must contain only one choice. 
    E.g. `"answer_text"`: `"Justo consectetur ullamcorper nec accumsan erat"`
    + if value of `"question_type"` - `"select_multiple"`, your answer must contain more than one choice. 
    E.g. `"answer_text"`: `"Morbi a justo erat, Nunc faucibus enterdum"`
    + the number of answers must be equal to the number of questions
    + set `"is_anonymous"` if needed (default `false`)
## GET /api/results/\<int:pk>/
Get a list of selected answers
+ ### URL parameters
    + `<int:pk>` - id of a user
* ### Response 200

```
[
    {
        "id": 1,
        "poll": {
            "id": 1,
            "name": "Poll #1",
            "start_date": "2021-03-17T15:42:11+03:00",
            "finish_date": "2021-03-19T15:42:14+03:00",
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis sed."
        },
        "answers": [
            {
                "question": {
                    "id": 3,
                    "question_text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                    "choices": "Morbi a justo erat, Nunc faucibus enterdum, Aliquam a id vel eros, In auctor placerat, Integer ac odio sed ut turpis",
                    "question_type": "select_multiple",
                    "created": "2021-03-17T15:43:12.782740+03:00",
                    "poll": 1
                },
                "answer_text": "Morbi a justo erat, Nunc faucibus enterdum"
            },
    ...
    ]
    "is_anonymous": false,
    "created": "2021-03-17T19:15:58.208982+03:00"
}
]
```
