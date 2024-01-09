
<h2>Usage</h2>
<p>
Execute src/main.py

First run generates **shovel.ini**

Get help with **--help** flag
</p>

<h2>Extras</h2>
<p>
Place videos you desire to be on the bottom in stash/assets/bottoms

Place background music in stash/assets/music

Place overlays in stash/assets/overlays, feel free to edit with software of your choice
</p>

<h2>Requirements</h2>
<ul>
    <li>Python enviroment satisfying requirements.txt</li>
    <li>imagemagick</li>
    <li>wkhtmltopdf</li>
    <li>Arial.ttf</li>
</ul>

<h2>Generating content</h2>
<ul>
    <li>Set instances of use_placeholder in shovel.ini to False as desired</li>
    <li>Supply google client secrets for tts in auth/google</li>
    <li>Supply OpenAI api key and model for script generation in shovel.ini</li>
    <li>Supply Stability api key for image generation in shovel.ini</li>
</ul>
<p>
It is recommended while configuring that you set use_placeholder to False one at a time
</p>


<h2>Uploading content to Youtube</h2>
<ol>
    <li>Create project on Google Cloud Platform</li>
    <li>Enable YouTube Data API v3</li>
    <li>Download OAuth 2.0 client secrets</li>
    <li>Place client secrets in auth/youtube</li>
    <li>Set do_not_upload to False in shovel.ini </li>
</ol>
<p>
Upload videos are your own discretion, we do not condone abuse
</p>
