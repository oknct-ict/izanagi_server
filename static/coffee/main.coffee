$(() ->
  editor = CodeMirror.fromTextArea(document.getElementById("editor"),
    {
      lineNumbers: true,
      mode: "text/x-vb",
      matchBrackets: true,
    }
  )
  showToast = (text) ->
    toast = $('<div class="toast fade"><button type="button" class="close" data-dismiss="alert"></button><div class="toast-body"><p>' + text + '</p></div>')
    $("#alerts-container").append(toast.addClass("in"))

  class IzanagiWebSocket
    @SERVER_URL = "ws://nado.oknctict.tk:5000/websock/ide/"
    
    constructor: (receiver, error) ->
      receiver ||= () -> 0
      error ||= () -> 0
      @_websocket = new WebSocket(IzanagiWebSocket.SERVER_URL)
      @_websocket.onerror = error
      @_websocket.onmessage = (event) ->
        receiver JSON.parse(event.data)
    sendJSON: (data) ->
      @_websocket.send JSON.stringify(data)

  class IzanagiConnection
    class User
      constructor: (@userId = null, @sessionId = null) ->
      setUser: (userId, sessionId) ->
        if @userId != null
          @onLogout @userId, @sessionId
        if userId != null
          @onLogin userId, sessionId
        @userId = userId
        @sessionId = sessionId
      onLogout: () ->
      onLogin: () ->

    class Project
      @STATE_READY    = 0
      @STATE_CREATING = 1
      @STATE_RENAMING = 2
      @STATE_DELETING = 3
      @STATE_EMPTY    = 4
      @ERROR_ALREADY_EXISTS = -2

      constructor: (@projectName = "", @projectId = null) ->
        if @projectId == null
          @state = Project.STATE_EMPTY
        else
          @state = Project.STATE_READY
      create: (conn) ->
        if @state == Project.STATE_READY
          deferred = $.Deferred()
          deferred.reject Project.ERROR_ALREADY_EXISTS
          deferred.promise()
        else
          @state = Project.STATE_CREATING
          conn._sendCommand("pro_create", {
            project_name: @projectName
          }).done((msg) =>
            @projectId = msg.data.project_id
            @state = Project.STATE_READY
          )
      rename: (conn, projectName) ->
        @state = Project.STATE_RENAMING
        conn._sendCommand("pro_rename", {
          project_id: @projectId,
          project_name: projectName
        }).done((msg) =>
          @projectName = projectName
          @state = Project.STATE_READY
        ).fail(() =>
          @state = Project.STATE_READY
        )
      delete: (conn) ->
        @state = Project.STATE_DELETING
        conn._sendCommand("pro_delete", {
          project_id: @projectId,
        }).done((msg) =>
          @projectName = ""
          @projectId = null
          @state = Project.STATE_EMPTY
        ).fail(() =>
          @state = Project.STATE_EMPTY
        )
    class File
      constructor: (@projectId = null, @fileName = "", @dir = "/", @code = "", @fileId = null) ->
      save: (conn) ->
        conn._sendCommand("save", {
          file_name: @fileName,
          project_id: @projectId,
          dir: @dir,
          code: @code,
        }).done((msg) =>
          @fileId = msg.data.file_id
        )
      renew: (conn) ->
        conn._sendCommand("renew", {
          file_id: @fileId,
          code: @code
        })
      open: (conn) ->
        conn._sendCommand("open", {
          file_id: @fileId
        }).done((msg) =>
          @code = msg.data.code
        )
      
    @CONNECTION_TYPE = "ide"
    @DEFAULT_TIMEOUT = 5000
    @ERROR_TIMEOUT = -1
    @MAX_REQUEST_ID = 10000

    constructor: () ->
      @_requestId = 0
      @_user = new User()
      @_eventHandlers = {}
      @_izanagiWebSocket = new IzanagiWebSocket(
        (msg) =>
          if msg.request_id of @_eventHandlers
            @_eventHandlers[msg.request_id](msg)
            delete @_eventHandlers[msg.request_id]
          0
        , () ->
          showToast "please reload this web page"
      )
      @_validResponse = (msg, command) ->
        msg.data.result < 100 and msg.command == command + "_RES"
      @_makePacket = (command, data) ->
        rid = @_requestId
        @_requestId = (@_requestId + 1) % IzanagiConnection.MAX_REQUEST_ID
        if @_user._sessionId == null
          sid = ""
        else
          sid = @_user._sessionId
        {
          type: IzanagiConnection.CONNECTION_TYPE,
          session_id: sid,
          command: command + "_REQ",
          request_id: rid,
          data: data
        }
      @_sendCommand = (command, data = {}, timeout = IzanagiConnection.DEFAULT_TIMEOUT) ->
        deferred = $.Deferred()
        timerId = setTimeout(() ->
          deferred.reject(IzanagiConnection.ERROR_TIMEOUT)
        , timeout)
        @_eventHandlers[@_requestId] = (m) =>
          if @_validResponse m, command
            deferred.resolve m
          else
            deferred.reject m.data.result
          clearTimeout timerId
        @_izanagiWebSocket.sendJSON @_makePacket(command, data)
        deferred.promise()
      0
    login: (userId, password) ->
      @_sendCommand("login", {
        user_id: userId,
        password: password,
      }).done((msg) =>
        @_user.setUser userId, msg.session_id
      ).fail((error) =>
        @_user.setUser null, null
      )
    register: (userId, password, email, grade) ->
      @_sendCommand("register", {
        user_id: userId,
        password: password,
        address: email,
        grade: grade,
      }).done((msg) =>
        @_user.setUser userId, msg.session_id
      ).fail((error) =>
        @_user.setUser null, null
      )
    getProjects: () ->
      @_sendCommand("pro_list", {
      })
    createProject: (projectName) ->
      @_sendCommand("pro_create", {
        project_name: projectName
      })
    renameProject: (projectId, projectName) ->
      @_sendCommand("pro_rename", {
        project_id: projectId,
        project_name: projectName
      })
    deleteProject: (projectId) ->
      @_sendCommand("pro_delete", {
        project_id: projectId
      })
    saveFile: (projectId, dirName, fileName, code) ->
      @_sendCommand("save", {
        file_name: fileName,
        project_id: projectId,
        dir: dirName,
        code: code
      })
    updateFile: (fileId, code) ->
      @_sendCommand("renew", {
        file_id: fileId,
        code: code
      })
    openFile: (fileId) ->
      @_sendCommand("open", {
        file_id: fileId
      })
    deleteFile: (fileId) ->
      @_sendCommand("delete", {
        file_id: fileId
      })
    getFiles: (projectId) ->
      @_sendCommand("list", {
        project_id: projectId
      })
    renameFile: (fileId, fileName) ->
      @_sendCommand("rename", {
        file_id: fileId,
        file_name: fileName
      })
    redirFile: (fileId, dir) ->
      @_sendCommand("redir", {
        file_id: fileId,
        dir: dir
      })
    getFileInfo: (fileId) ->
      @_sendCommand("info", {
        file_id: fileId
      })
    setOnLogin: (handler) ->
      @_user.onLogin = handler
    setOnLogout: (handler) ->
      @_user.onLogout = handler

  con = new IzanagiConnection()
  con.setOnLogin (userId, sessionId) ->
    showToast "Welcome " + userId
    $("#icon-btn_register").addClass("disable")
    $("#icon-btn_login").addClass("disable")
    $("#icon-btn_project").removeClass("disable")

  con.setOnLogout (userId, sessionId) ->
    showToast "Bye " + userId
    $("#icon-btn_register").removeClass("disable")
    $("#icon-btn_login").removeClass("disable")
    $("#icon-btn-project").addClass("disable")

  $("#projectModal").on "shown", () ->
    con.getProjects().done(() ->
    )
  $("#btn-login").click(() ->
    userId = $("#txt-login_user_id").val()
    password = $("#txt-login_passwd").val()
    con.login(userId, password).done(() ->
      $("#loginModal").modal "hide"
    ).fail(() ->
      showToast "login failed"
    )
  )

  $("#btn-register").click(() ->
    userId = $("#txt-register_user_id").val()
    password = $("#txt-register_passwd").val()
    passwordConfirm = $("#txt-register_passwd_confirm").val()
    email = $("#txt-register_email").val()
    school = parseInt $("#select-register_school").val()
    grade = parseInt $("#select-register_grade").val()

    if password != passwordConfirm
      showToast "password incorrect"
      return 0

    con.register(userId, password, email, school * 10 + grade).done(() ->
      $("#registerModal").modal "hide"
    ).fail(() ->
      showToast "registration failed"
    )
  )
)
