# DC Themer to-do

## Functionality

| Item | Details | Priority | Notes |
|---|---|---|---|
| Scheme export | Allow to export scheme from current DC config. | High ||
| User config | - ~~Implement config in json format.~~<br>- ~~Create default, if doesn't exist, on app start.~~<br>- In-app window to modify.<br>- ~~Versioning, in case new config values appear in the future.~~ | Medium ||
| Theme verification | Before applying, theme files should be verified against schemas (cfg, json, xml).<br>Some of it is already implemented in unit tests.<br>Schemas should be in separate files. | Medium ||
| Default config creation summary | Add info box. | Low | If displayed before root window, root will loose focus. Need to be implemented with different approach. |
| **doublecmd.xml** version verification | - Config key to enable/disable verification (?).<br>- Separate menu item to run verification. | Low ||
| Scheme apply summary | Detailed message with performed actions, e.g. DC config backup. | Low ||

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