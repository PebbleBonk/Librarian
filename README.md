# DataLibrarian
A simple utility to help manage creation of training data from multiple sources


---
## 1. Description
Collating data is cumbersome. Maintaining it is difficult. You want to collect plenty of data everywhere.
This is a simple server solution to put up every time you need users to submit their versions of labels.

Originally a social distancing project

### 1.1. Features
1. Runs as a microservice with a simple API
2. Provides handle for mongoDB (label information)
3. Provides handle for S3 bucket (larger data, e.g. images)
4. Provides methods for local saving

The service processes two types of objects: __labels__ and __data__. The __labels__ are sent in the url endpoints and the __data__ in request body.

**NOTE:**
> This shuold be changed to be multipart POST instead

---
## 2. Librarian
Librarian is the main application running the show. It runs as a simple Flask app. It takes data as an input, validates it with `Validator`s, and passes the validated datas to `Actor`s to be processed.

The basic pipeline when an annotation upload request is received:

1. Run label validators on label(s)
2. Run data validators for data
3. Run cross validators for label(s) and data
4. If unsuccessfull, abort
5. Run label actions
6. Run data actions
7. Return success

**NOTE:**
> The service sending the information is responsible for matching the data to given schematic


### 2.1. Configuration
The Librarian needs to be configured on how what type of data to expect, how to validate it and how to act on it. The configuration happens using dictionaries.

Practically, you have three methods to configure the service: json files, dotenv files and environmental variables. The first one is most readable, but the last one allows deployment of multiple configurations without having to modify or branch the code itself in, for example, docker containers or heroku apps.

**NOTE:**
> In future veriosns, the json config file could be provided as an url

#### 2.1.1. Configuring Input
Input defines what sort of data the service expects. The variables `type` and `tag` should be set accordingly. The values for the configurations should be strings. For example:

```json
    "INPUT_CONFIG": {
        "type": "base64",
        "tag": "image"
    }
```

Run the following command to see the list of available options:
```
$ python librarian_cli.py describe --inputs
```

#### 2.1.2. Configuring Validators
Validators check if the data obtained is valid. This can save some resources on storage and access, and ease the processing needed later.

The variables you need to set are `LABEL_VALID_CONFIG`, `DATA_VALID_CONFIG` and `CROSS_VALID_CONFIG`. The values for configurations should be a dict with the keys `validator`, `args` and `kwargs`. The `validator` (str) value defines which type of validator is used, and the values in `args` (list) and `kwargs` (list) are passed to the Validator init function as arguments. For example:

```json

    "DATA_VALID_CONFIG": [{
        "validator": "img",
        "args": [
            0
        ],
        "kwargs": {
            "w": 0
        }
    }]

```

Would create a validator for image as `ImageValidator(0, w=0)`.

**NOTE** that the cross validator is similar to a normal validator, but processes both data and labels.

**NOTE:**
> Make sure that the args and kwargs do not overlap!

Run the following commands to see the list of available options:
```
$ python librarian_cli.py describe --validators
$ python librarian_cli.py describe --xvalidators
```

**NOTE:**
> You can also chain several validators by simply including multiple configuration dicts for the _VALID_CONFIG list. The validators included will be executed in that order.

#### 2.1.3. Configuring Actors
Actors finally process the data if it passes all the validations. This can mean for example uploading to a cloud storage, or saving the file locally.

The variables you need to set are `LABEL_ACTOR_CONFIG` and `DATA_ACTOR_CONFIG`. The values for configurations should be a dict with the keys `actor`, `args` and `kwargs`. The `actor` (str) value defines which type of actor is used, and the values in `args` (list) and `kwargs` (list) are passed to the Actor init function as arguments.

```json
    "LABEL_ACTOR_CONFIG": [{
        "actor": "json",
        "args": [
            "local/results.json"
        ]
    },
    {
        "actor": "file",
        "args": [
            "local/results/"
        ]
    }],
    "DATA_ACTOR_CONFIG": [{
        "actor": "image",
        "args": [],
        "kwargs": {
            "directory": "local/images/"
        }
    }]

```

**NOTE:**
> Make sure that the args and kwargs do not overlap!

Run the following command to see the list of available options:
```
$ python librarian_cli.py describe --actors
```

**NOTE:**
> You can also chain several actors by simply including multiple configuration dicts for the _DATA_CONFIG list. The actors included will be executed in that order.



### 2.2. Launching
The Librarian sevice can be launched in three ways:
1. With local .env file variables
    ```
    $ python librarian_cli.py launch --dotenv <FILE>
    ```
2. With local json config file
    ```
    $ python librarian_cli.py launch --json <FILE>
    ```
3. With environmental variables (default)
    ```
    $ python librarian_cli.py launch
    ```

For more info and options how to launch the service run:
```
$ python librarian_cli.py launch --help
```




---
## 3. Deployment
The tool was made to streamline deployment of training data collection services. For example, to collect image annotation data, we could define the config variables to be passed on to e.g. heroku as follows:

```sh
INPUT_CONFIG = '{"type": "base64","tag": "image"}'
LABEL_VALID_CONFIG = '[{"validator": "type","args": [{"filename": "str","x": "int","y": "int"}]}]'
DATA_VALID_CONFIG = '[{"validator": "img","kwargs": {"h": 0,"w": 0}}]'
LABEL_ACTOR_CONFIG = '[{"actor": "mongo","args": ["<user>","<pswd>","<url>","<db>","<col>"]}]'
DATA_ACTOR_CONFIG = '[{"actor": "S3","args": ["<access_key>","secret_key>","<bucket_name>","images/",""]}]'
CROSS_VALID_CONFIG = '[]'
```

A `Librarian`  instance with such a configuration would expect a base64 encoded string as an __input__ on request, under a "image" name. __Validation__ would assert that the labels passed in url endpoints are "filename" as `str` and "x" and "y" as a `int`, as well as that the image passed in the input is a valid image file, with any dimension restrictions.

If all the condiftions are met, the labels are then uploaded to __mongo__ to the collection `<col>` in database `<db>` and the image uploaded to __S3__ to bucket `<bucket_name>` with a prefix of "images/ and without any suffix.


## 4. Example
The first application using this can be found in [CropperHead](http://cropper-head.herokuapp.com), where it is used to collect training data from users in form of images and values about the crop on them.

---
## 5. License
MIT