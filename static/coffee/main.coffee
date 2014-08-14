$(() ->
  editor = CodeMirror.fromTextArea(document.getElementById("editor"),
    {
      lineNumbers: true,
      mode: "text/x-vb",
      matchBrackets: true,
    }
  )

  ws = new WebSocket("ws://nado.oknctict.tk:5000/websock/ide/")
  session_id = null

  ws.onclose = ws.onerror = (error) ->
    alert "please reload web page"

  ws.onmessage = (event) ->
    msg = JSON.parse(event.data)
    console.log msg
    if msg.command == "login_RES"
      if msg.data.result < 100
        session_id = msg.session_id
        $("#loginModal").modal("hide")
        0
      else
        $("#loginModal").modal("show")
        0

  make_msg = (command, data) ->
    if session_id == null
      sid = ""
    else
      sid = session_id

    return JSON.stringify({
      type: "ide",
      session_id: sid,
      command: command + "_REQ",
      data: data
    })

  $("#btn-login").click(() ->
    user_id = $("#user_id").val()
    passwd = $("#passwd").val()
    msg = make_msg("login", {
      user_id: user_id,
      password: passwd
    })
    console.log msg
    ws.send(msg)
  )

  $("#btn-upload").click(()->
    if session_id == null
      $("#loginModal").modal("show")
      return
  )
)

