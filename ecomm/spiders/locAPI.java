

JSONObject objInput=new JSONObject(inStringJson);

for(int i=0;i<objInput.length();i++){

String attr=objInput.getString("attr");
String value=objInput.getString("value");

MediaType mediaType = MediaType.parse("application/json;charset=UTF-8");
RequestBody body = RequestBody.create(mediaType, "{\"inArray\":["+value+"],\"REV-APP-ID\":\"webapp\",\"REV-API-KEY\":\""+apikey+"\",\"domain\":5,\"targetLanguage\":\""+language+"\",\"inputLanguage\":\"hindi\",\"webSdk\":0}");
Request request = new Request.Builder()
 .url("http://api.reverieinc.com/localization/localizeJSON")
 .post(body)
 .addHeader("content-type", "application/json;charset=UTF-8")
 .build();

com.squareup.okhttp.Response response = client.newCall(request).execute();
ResponseBody x=(ResponseBody) response.body();
JSONObject test=new JSONObject(x.toString());
JSONObject test1=new JSONObject();
JSONArray testArray=new JSONArray();
testArray=test.getJSONArray("outArray");
test1=testArray.getJSONObject(0);
String attrVal=test1.getString("inString");
String attrTvalue=test1.getString("transResponse");
outJsonObject.put("attr", attrVal);
outJsonObject.put("TransValue", attrTvalue);

}
