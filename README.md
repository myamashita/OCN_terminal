# OCN_terminal
Small plugin to open prompt into file location.

This is an alpha release, use with care, feedback & code welcome!

# Menu
There are 4 menu items under `Preferences\Package Settings\OCN_terminal`:

- `Settings - Default` - Open a default setting to provide a user prompt
- `Settings - User` - Open a custom setting to provide a user prompt
- `Key Bindings - Default` - Open a default key binding 
- `Key Bindings - User` - Open a custom key binding 

# Usage

 - **Open Terminal at File**
     Press *ctrl+shift+t*
     
# Examples

#### Cmd on Windows

```js
{
  // Replace with your own path to cmd.exe
  "terminal": "C:\\Windows\\System32\\cmd.exe",
  "parameters": ["/START", "%CWD%"]
}
```