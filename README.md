# Streamlink Fansly Plugin

## Install

- Copy the [fansly.py](fansly.py) file into one of the [sideload directories](https://streamlink.github.io/cli/plugin-sideloading.html)

## Setup

Follow these instructions to get your token and user agent: <https://github.com/Avnsx/fansly-downloader/wiki/Get-Started#manual-set-up>.

Or formatted nicely to copy/paste into `config.fansly`

```js
console.clear(); 
const activeSession = localStorage.getItem("session_active_session");
const { token } = JSON.parse(activeSession); 
console.log(`fansly-header-auth=${token}\nfansly-header-user-agent=${navigator.userAgent}`)
```

Put values into the example [fansly config format](fansly.config.example) and copy to `%APPDATA%\streamlink\config.fansly`

## Usage

Only user_id is set up right now, which should just be a bunch of numbers 0-9. If you click on "live" on their profile, you will probably get live/username. You should be able to get the url with user_id from the home page.

```powershell
streamlink fansly.com/<user_id> best
```