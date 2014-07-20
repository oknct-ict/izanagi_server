$(() ->
  editor = CodeMirror.fromTextArea(document.getElementById("editor"),
    {
      lineNumbers: true,
      mode: "text/x-vb",
      matchBrackets: true,
    }
  )
  ws = new WebSocket("ws://nado.oknctict.tk:8000/echo")
  $("#btn-upload").click(()->
    console.log editor.getValue()
  )
)

