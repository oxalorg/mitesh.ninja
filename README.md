Simple api queries for my personal use.
=======================================

## Modules

### Static form contact

Embed the following snippet in any website, static or dynamic.

```html
<form method="POST" action="api.mitesh.ninja/<YOUR-EMAIL-ID@DOMAIN>/">
    <!-- This field allows the user to mention a REPLY-TO email address -->
    <!-- If it is not present, it will default to garabge -->
    <input type="email" name="senderEmail" value="DEFAULT VALUE HERE">
    <!-- If name/default not present, it will default to 'ANONYMOUS' -->
    <input type="text" name="senderName" value="DEFAULT NAME HERE">
    ...
    ...
    ...
    <!-- All input tags should have a 'name' attribute present -->
</form>
```

To Do:

* [ ]: Add HTTPS support
* [ ]: Add authentication before starting to send emails
* [ ]: Limit emails sent to 20/day to avoid spam
* [ ]: All data stored must be securely hashed

### Automated notifier

Coming soon..
