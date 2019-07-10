var LANG_OBJ = {};

nethserver.fetchTranslatedStrings(function(data) {
  LANG_OBJ = data;
  $(document).trigger("nethserver-loaded");
});

function _(string) {
  return LANG_OBJ[string];
}
