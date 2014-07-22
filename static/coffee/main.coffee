$(() ->
  editor = CodeMirror.fromTextArea(document.getElementById("editor"),
    {
      lineNumbers: true,
      mode: "text/x-vb",
      matchBrackets: true,
    }
  )
  ws = new WebSocket("ws://nado.oknctict.tk:5000/echo")
  $("#btn-upload").click(()->
    #console.log editor.getValue()
    msg = { type: "ide", command: "SYN", message: editor.getValue() }
    ws.send(JSON.stringify(msg))
  )
)

