// Rename to settings.js and replace the service account id, and calendar IDs with your own
// Delete googleapi-key-sample.json and insert googleapi-key.json from your google api console
const SERVICE_ACCT_ID = "XXXX@XXXX.iam.gserviceaccount.com";
const key = require("./googleapi-key.json").private_key;
const TIMEZONE = "UTC+01:00";
const CALENDAR_ID_LIST = {
  definitive: "XXX@group.calendar.google.com",
  cancelled: "XXX@group.calendar.google.com",
  inquiry: "XXX@group.calendar.google.com"
};

module.exports.serviceAcctId = SERVICE_ACCT_ID;
module.exports.key = key;
module.exports.timezone = TIMEZONE;
module.exports.calendarIdList = CALENDAR_ID_LIST;
