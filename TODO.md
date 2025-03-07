# DC Themer to-do

## Functionality

| Item | Details | Priority | Notes |
|---|---|---|---|
| Scheme export | - ~~Export from current DC config.~~<br>- ~~Warning: scheme with the same name already exists.~~<br>- ~~Warning: name is empty.~~<br>- Warning: ~~name should contain allowed chars only.~~<br>- Save files only if successfully generated. | High ||
| Scheme apply | - Only save files if all are successfully updated.<br>- Detailed message with performed actions, e.g. config backup. | Medium ||
| User config | - ~~Implement config in json format.~~<br>- ~~Create default, if doesn't exist, on app start.~~<br>- In-app window to modify.<br>- ~~Versioning, in case new config values appear in the future.~~ | Medium ||
| Theme verification | Before applying, theme files should be verified against schemas (cfg, json, xml).<br>Some of it is already implemented in unit tests.<br>Schemas should be in separate files. | Medium ||
| Linux compatibility | Adjust code to run in Linux, including WSL machines. | Medium | - Line endings in config files.<br>- App icon format (ico is Windows specific). |
| Scheme delete | Button or menu item to delete selected scheme files. | Low ||
| Default config creation summary | Add info box. | Low | If displayed before root window, root will loose focus. Need to be implemented with different approach. |
| **doublecmd.xml** version verification | - Config key to enable/disable verification (?).<br>- Separate menu item to run verification. | Low ||

## Testing

| Item | Details |
| --- | --- |
| Compatibility | Test app on multiply Python versions. |

## CI/CD

| Item | Details |
| --- | --- |
| Gitlab CI pipeline | Create. Should run quality gates and prepare Windows package for release. |

## Documentation

| Item | Details |
| --- | --- |
| README | Add information about supported Python version (3.12.x). |
| User documentation | Document all user features. |