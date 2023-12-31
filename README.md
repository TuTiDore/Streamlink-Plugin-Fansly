# Streamlink Fansly Plugin

## Install

- pip install [cloudscraper](https://pypi.org/project/cloudscraper)
  - For streamlink on Windows with an embedded Python environment, you need to specify the target `--target=<StreamLinkInstallPath>\pkgs` or you will get `ModuleNotFoundError`.
- Copy the [fansly.py](fansly.py) file into one of the [sideload directories](https://streamlink.github.io/cli/plugin-sideloading.html)
  - Or run the python script [Copy to appdata](copy_to_appdata.py)

## Setup

Follow these instructions to get your token and user agent: <https://github.com/Avnsx/fansly-downloader/wiki/Get-Started#manual-set-up>.

Put values into the example [fansly config](config.fansly.example) and copy to `%APPDATA%\streamlink\config.fansly`

## Usage

Only user_id is set up right now, which should just be a bunch of numbers 0-9. If you click on "live" on their profile, you will probably get live/username. You should be able to get the url with user_id from the home page.

```powershell
streamlink fansly.com/<user_id> best
```