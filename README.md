<h2>Usage</h2>
<p>
    Execute <code>src/main.py</code>.
    <br>
    The first run generates <strong>shovel.ini</strong>.
    <br>
    For help, use the <strong>--help</strong> flag.
</p>

https://github.com/meshbound/Shovel/assets/60497577/306a3117-8ce5-4a92-9eec-22495f650fd0

<h2>Extras</h2>
<p>
    Place videos you want at the bottom in <code>stash/assets/bottoms</code>.
    <br>
    Add background music to <code>stash/assets/music</code>.
    <br>
    Include overlays in <code>stash/assets/overlays</code> and customize them with your preferred software.
</p>

<h2>Requirements</h2>
<ul>
    <li>Python environment satisfying <code>requirements.txt</code>.</li>
    <li>Install <code>imagemagick</code>.</li>
    <li>Install <code>wkhtmltopdf</code>.</li>
    <li><code>Arial.ttf</code> font file is required.</li>
</ul>

<h2>Generating Content</h2>
<ul>
    <li>Set instances of <code>use_placeholder</code> in <strong>shovel.ini</strong> to <code>False</code> as needed.</li>
    <li>Supply Google client secrets for TTS in <code>auth/google</code>.</li>
    <li>Provide OpenAI API key and model for script generation in <strong>shovel.ini</strong>.</li>
    <li>Supply Stability API key for image generation in <strong>shovel.ini</strong>.</li>
</ul>
<p>
    While configuring, it's recommended to set <code>use_placeholder</code> to <code>False</code> one at a time.
</p>

<h2>Uploading Content to YouTube</h2>
<ol>
    <li>Create a project on Google Cloud Platform.</li>
    <li>Enable YouTube Data API v3.</li>
    <li>Download OAuth 2.0 client secrets.</li>
    <li>Place client secrets in <code>auth/youtube</code>.</li>
    <li>Set <code>do_not_upload</code> to <code>False</code> in <strong>shovel.ini</strong>.</li>
</ol>
<p>
    Upload videos at your discretion; we do not condone abuse.
</p>
