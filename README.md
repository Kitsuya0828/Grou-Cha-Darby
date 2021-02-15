# Grou-Cha-Darby

This website enables you to make a Bar Chart Race with your LINE chat hisory.

URL : [https://grouchadarby0210.herokuapp.com/](https://grouchadarby0210.herokuapp.com/)

# DEMO

Below are the website overview

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/832523/181bacdb-dba1-937d-ab71-32529f60eb06.png">
<table>
<tr>
<td><img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/832523/189f0810-1b0f-bb69-c5f2-e19a66e1da76.png"></td>
<td><img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/832523/c4f17e40-9893-a351-f783-8d8a3027b2f2.png"></td>
</tr>
</table>

# Features


# Requirement

* Python 3.8.5
* bar-chart-race 0.1.0
* ffmpeg 1.4
* ffmpeg-python 0.2.0
* japanize-matplotlib 1.1.3
* matplotlib 3.3.2
* numpy 1.18.5
* pandas 1.1.2
* Pillow 7.2.0
* plotly 4.14.3
* streamlit 0.76.0


# Installation

```bash
pip install bar-chart-race
pip install ffmpeg
pip install ffmpeg-python
pip install japanize-matplotlib
pip install matplotlib
pip install numpy
pip install pandas
pip install Pillow
pip install plotly
pip install streamlit
```

# Usage

```bash
git clone https://github.com/Kitsuya0828/Grou-Cha-Darby.git
cd Grou-Cha-Darby
```
You can run it locally from the command prompt just using the command:

```bash
streamlit run app.py
```

This will spin up a webserver on your local machine and display the application in your browser. You can do your testing here to make sure everything works fine.

The next step is deploying the application on Heroku.
Heroku requires you to create a new GitHub repository for your application and link it with Heroku. This repository should contain all the artifacts needed for your projects.

Below are the main components:
1. app.py : This is my python code file.
2. requirements.txt : This file contains all the environmental requirements.
3. setup.sh : This file is required to run Streamlit in Heroku.
4. Procfile : This is a file required by Heroku to run the application. It basically tells Heroku what command to execute.
5. logo.png : This is an image for the logo of the website.
6. mainimg.png : This is an image for the key visual of the website.

For more details, please refer to the link below:

[NLP and Streamlit on Heroku. How I deployed my Streamlit based NLP… | by Rahul Bhattacharya | Towards Data Science](https://towardsdatascience.com/nlp-and-streamlit-on-heroku-5ebb56d6a57f)

# Note

FFmpeg is a collection of libraries and tools to process multimedia content such as audio, video, subtitles and related metadata.

To add Heroku buildpack for ffmpegm, run the following from the heroku command line:

```bash
heroku buildpacks:add --index 1 https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
```

See also:

[jonathanong/heroku-buildpack-ffmpeg-latest - Buildpacks - Heroku Elements](https://elements.heroku.com/buildpacks/jonathanong/heroku-buildpack-ffmpeg-latest)


# Author

* Kitsuya Azuma
* Tohoku University
* kitsuyaazuma@gmail.com

# License

"Grou-Cha-Darby" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).


Thank you!
