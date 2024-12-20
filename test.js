parsedSettings: {
    "function":"run",
    "source":"function run(inputContent) {
        inputContent = JSON.parse(inputContent);
        emailAtendente = inputContent[\"agentIdentity\"].split(\"@\",1)[0].replace(\"%40\", \"@\");
        return emailAtendente;
        }",
    "inputVariables":["input.content"],
    "outputVariable":"emailAtendente",
    "LocalTimeZoneEnabled":false
}