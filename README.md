# DataLibrarian
A simple utility to help manage creation of training data from multiple sources


---
## 1. Description
Collating data is cumbersome. Maintaining it is difficult. You want to colelct plenty of data everywhere.
This is a simple server solution to put up every time you need users to submit their versions of labels.

Originally a social distancing project

### 1.1. Features
1. Runs as a microservice with a simple API
2. Provides handle for mongoDB (label information)
3. Provides handle for S3 bucket (larger data, e.g. images)
4. Provides methods for local saving

The service processes two types of objects: __labels__ and __data__. The __labels__ are sent in the url endpoints and the __data__ in request body.


---
## 2. Librarian
Librarian is the main application running the show. It runs as a simple Flask app. It takes data as an input, validates it with `Validator`s, and passes the validated datas to `Actor`s to be processed.

The basic pipeline when an annotation upload request is received:

1. Run label validator on label(s)
2. Run data validator for data
3. Run cross validator for label(s) and data
4. If unsuccessfull, abort
5. Run label action
6. Run data action
7. Return success

**NOTE:**
> The service sending the information is responsible for matching the data to given schematic


### 2.1. Configuration
The Librarian needs to be configured on how what type of data to expect, how to validate it and how to act on it. The configuration happens using dictionaries.

Practically, you have three methods to configure the service: json files , environmental variables, and command line arguemtns. The first one is most readable, but the latter two allow deployment of multiple configurations without having to modify or branch the code itself in, for example, docker containers or heroku apps.


#### 2.1.1. Configuring Input
Input defines what sort of data the service expects. The variables `DATA_TYPE` and `DATA_TAG` should be set accordingly. The values for the configurations should be strings. For example:

```json
    "DATA_TYPE": "file",
    "DATA_TAG": "image",
```

Run the following command to see the list of available options:
```
python app.py describe_input_options
```

#### 2.1.2. Configuring Validators
Validators check if the data obtained is valid. This can save some resources on storage and access, and ease the processing needed later.

The variables you need to set are `LABEL_VALID_CONFIG`, `DATA_VALID_CONFIG` and `CROSS_VALID_CONFIG`. The values for configurations shuold be a dict with the keys `validator` and `args`; for example:

```json
{
    "LABEL_VALID_CONFIG": {
        "validator": "type",
        "args": [
            {
                "filename": "str",
                "class": "int"
            }
        ]
    },
    "DATA_VALID_CONFIG": {
        "validator": "img",
        "args": [
                0,
                0
        ]
    },
    "CROSS_VALID_CONFIG": {
        "validator": "none",
        "args": []
    }
}
```
**NOTE** that the cross validator is similar to a normal validator, but processes both data and labels.

Run the following commands to see the list of available options:
```
python app.py describe_validator_options
python app.py describe_crossvalidator_options

```

#### 2.1.3. Configuring Actors
Actors finally process the data if it passes all the validations. This can mean for example uploading to a cloud storage, or saving the file locally.

The variables you need to set are `LABEL_ACTOR_CONFIG`, `DATA_ACTOR_CONFIG` and `CROSS_ACTOR_CONFIG`. The values for configurations shuold be a dict with the keys `actor` and `args`; for example:

```json
{

    "LABEL_ACTOR_CONFIG": {
        "actor": "json",
        "args": [
            "labels.json"
        ]
    },
    "DATA_ACTOR_CONFIG": {
        "actor": "S3",
        "args": [
            "SampleBucket",
            "images",
            ".jpg"
        ]
    }
}
```
Run the following command to see the list of available options:
```
python app.py describe_actor_options
```

### 2.2. Launching
The Librarian sevice can be launched in three ways:
1. With environmental variables
2. With local json config file
3. With command line parameters
see
```
python app.py --help
```

for more info how to launch the service


---
## 3. Deployment
The tool was made to streamline deployment of training data collection services. For example, to collect image annotation data, we could define the config variables to be passed on to e.g. heroku as follows:

```sh
DATA_TYPE = "file",
DATA_TAG = "image",
LABEL_VALID_CONFIG = '{"validator": "type","args": [{"filename": "str","class": "int"}]}'
DATA_VALID_CONFIG = '{"validator":"img","args":[0,0]}'
LABEL_ACTOR_CONFIG = '{"actor":"json","args":["labels.json"]}'
DATA_ACTOR_CONFIG = '{"actor":"S3","args":["SampleBucket","images/",""]}'
CROSS_VALID_CONFIG = '{"validator":"none","args":[]}'

```

A `Librarian`  instance with such a configuration would expect a file as an input on request, under a "image" name, would assert that the labels passed in url endpoints are "filename" as string and "class" as a integer, as well as that the image passed in the body as a file is a valid image file, with any dimensions.

If all the condiftions are met, the labels are then appended locally to the file `labels.json` and the image uploaded to S3 to bucket "SampleBucket" with a prefix of "images/ and without any suffix.


---
## 4. NOTES
- The config could be more human readable with kwargs instead of args
- Ability to chain validators and actors is coming

---
## 5. License
MIT