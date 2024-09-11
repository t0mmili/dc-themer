# DC Themer
A free open source application aiming to complement the functionality of Double Commander with a theme switcher.

## :fire: Key features
* Switch themes instantly with just one click.
* Backup DC configuration before applying new theme.
* Get everything done via readable GUI.
* Customize application configuration in json format.
* For other planned cool features check [TODO.md](TODO.md).

## :hammer: Stack
DC Themer is written in [Python 3](https://www.python.org/), with the [Tkinter](https://wiki.python.org/moin/TkInter) package for the GUI.

## :clipboard: Prerequisites
There are no special requirements to my knowledge.

For the time being DC Themer is released as Windows binary, but feel free to pull the source code and run/compile on other machines.

## :rocket: Quick start (Windows)
1. Download [DC Themer latest version](https://github.com/t0mmili/dc-themer/releases/latest).
2. Download [themes]((https://github.com/t0mmili/dc-themes)) from my other GitHub repo.
3. Put **schemes** folder next to **dc-themer.exe**.
4. Run **dc-themer.exe**.
5. For most cases the default configuration should be ok.  
   If your DC is located in custom folder, adjust these keys in **dc-themer.json**:
    ```json
    {
      ...
      "doubleCommander": {
        ...
        "configPaths": {
          "cfg": "%APPDATA%\\doublecmd\\doublecmd.cfg",
          "json": "%APPDATA%\\doublecmd\\colors.json",
          "xml": "%APPDATA%\\doublecmd\\doublecmd.xml"
        }
      },
      ...
    }
    ```
6. Profit!

## :muscle: Contribution
Contributions are greatly appreciated! If you want to report a bug or request a feature, please [open an issue](https://github.com/t0mmili/dc-themer/issues).

## :heart: Sponsorship
I create purely out of passion, in free time, on top of my day job as a Systems Engineer and a father.  
If you find my work useful and would like to express your gratitude and support further development, [throw in some coins](https://github.com/sponsors/t0mmili) 😉

##  :notebook: License
This project is licensed under the [MIT License](https://github.com/t0mmili/dc-themer/blob/main/LICENSE).

## :mag: See also
Please also have a look at other similar projects and support authors for the great job they are doing.

|||
|---|---|
| Double-Commander-Theme-Changer | https://github.com/delington/Double-Commander-Theme-Changer |
| DoubleCommanderColorScheme | https://github.com/andriitishchenko/DoubleCommanderColorScheme |