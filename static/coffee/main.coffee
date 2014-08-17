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
  event_handlers = {}



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

  send = (command, data, timeout) ->
    data ||= {}
    timeout ||= 5000

    msg = make_msg(command, data)
    deferred = $.Deferred()
    
    timer_id = setTimeout(() ->
      deferred.reject()
    , timeout)

    event_handlers[command + "_RES"] = (m) ->
      deferred.resolve(m)
      clearTimeout timer_id

    ws.send(msg)
    console.log "Send:"
    console.log msg
    return deferred.promise()

  show_toast = (text) ->
    toast = $('<div class="toast fade"><button type="button" class="close" data-dismiss="alert"></button><div class="toast-body"><p>' + text + '</p></div>')
    $("#alerts-container").append(toast.addClass("in"))
    
  ws.onerror = (error) ->
    show_toast "please reload this web page"

  ws.onmessage = (event) ->
    msg = JSON.parse(event.data)
    console.log "Receive:"
    console.log msg
    if msg.command of event_handlers
      event_handlers[msg.command](msg)
    0

  $("#projectModal").on("shown", () ->
    send("pro_list", {}).then(
      (msg) ->
        # succuses
        show_toast "pro_list passive"
      , () ->
        # fail
    )
  )

  $("#btn-login").click(() ->
    user_id = $("#txt-login_user_id").val()
    passwd = $("#txt-login_passwd").val()
    send("login", {
      user_id: user_id,
      password: passwd
    }).then(
      (msg) ->
        if msg.data.result < 100
          session_id = msg.session_id
          $("#loginModal").modal("hide")
        else
          session_id = null
          show_toast "login failed"
        0
      , () ->
        session_id = null
        show_toast "login timeout"
    )
  )

  $("#btn-register").click(() ->
    user_id = $("#txt-register_user_id").val()
    passwd = $("#txt-register_passwd").val()
    passwd_confirm = $("#txt-register_passwd_confirm").val()
    email = $("#txt-register_email").val()
    school = parseInt $("#select-register_school").val()
    grade = parseInt $("#select-register_grade").val()

    if passwd != passwd_confirm
      show_toast "password incorrect"
      return 0

    send("register", {
      user_id: user_id,
      password: passwd,
      address: email,
      grade: school * 10 + grade,
    }).then(
      (msg) ->
        if msg.data.result < 100
          session_id = msg.session_id
          $("#registerModal").modal("hide")
        else
          show_toast "registration failed"
      , () ->
        show_toast "registration timeout"
    )
  )
)

