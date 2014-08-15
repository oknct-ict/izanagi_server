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

  send = (msg) ->
    console.log msg
    ws.send(msg)

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

  show_toast = (text) ->
    toast = $('<div class="toast fade"><button type="button" class="close" data-dismiss="alert"></button><div class="toast-body"><p>' + text + '</p></div>')
    $("#alerts-container").append(toast.addClass("in"))
    
  ws.onerror = (error) ->
    show_toast "ページを読み込みなおしてください"

  ws.onmessage = (event) ->
    msg = JSON.parse(event.data)
    console.log msg
    if msg.command == "login_RES"
      if msg.data.result < 100
        session_id = msg.session_id
        $("#loginModal").modal("hide")
      else
        session_id = null
        show_toast "ログインに失敗しました"
    if msg.command == "register_RES"
      if msg.data.result < 100
        session_id = msg.session_id
        $("#registerModal").modal("hide")
      else
        show_toast "ユーザ登録に失敗しました"
    0

  $("#btn-login").click(() ->
    user_id = $("#txt-login_user_id").val()
    passwd = $("#txt-login_passwd").val()
    msg = make_msg("login", {
      user_id: user_id,
      password: passwd
    })
    send(msg)
  )

  $("#btn-register").click(() ->
    user_id = $("#txt-register_user_id").val()
    passwd = $("#txt-register_passwd").val()
    passwd_confirm = $("#txt-register_passwd_confirm").val()
    email = $("#txt-register_email").val()
    school = parseInt $("#select-register_school").val()
    grade = parseInt $("#select-register_grade").val()

    if passwd != passwd_confirm
      return 0

    msg = make_msg("register", {
      user_id: user_id,
      password: passwd,
      address: email,
      grade: school * 10 + grade,
    })
    send(msg)
  )
)

