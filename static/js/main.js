(function() {
  $(function() {
    var editor, ws;
    editor = CodeMirror.fromTextArea(document.getElementById("editor"), {
      lineNumbers: true,
      mode: "text/x-vb",
      matchBrackets: true
    });
    ws = new WebSocket("ws://nado.oknctict.tk:8000/echo");
    return $("#btn-upload").click(function() {
      var msg;
      msg = {
        type: "web",
        command: "SYN",
        message: editor.getValue()
      };
      return ws.send(JSON.stringify(msg));
    });
  });

}).call(this);
