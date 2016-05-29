My personal playground/training arena
======================================

[http://mitesh.ninja](http://mitesh.ninja)

## Modules

### Static form contact

Embed the following snippet in any website, static or dynamic.
When the use submits this form, all it's elements (with a name attribute) will be forwarded to your email address with a "REPLY-TO" option of the sender.

```html
<form method="POST" action="http://api.mitesh.ninja/form/sendForm/<YOUR-EMAIL-ID@DOMAIN>/">
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

* [ ] Add HTTPS support
* [ ] Add authentication before starting to send emails
* [ ] Limit emails sent to 20/day to avoid spam
* [ ] All data stored must be securely hashed

### Upload

Upload mutliple images, text, pdf files here: [mitesh.ninja/upload](http://mitesh.ninja/upload)

To Do:

* [ ] Add HTTPS support
* [ ] Add authentication
* [ ] restrict uploads to 50 files/hr
* [ ] restrict access using api tokens
* [ ] make a command line script to auto upload
    - [ ] add screenshot feature in it

### Automated notifier

Coming soon..
