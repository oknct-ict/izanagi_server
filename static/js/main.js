(function() {
  $(function() {
    var editor, make_msg, session_id, ws;
    editor = CodeMirror.fromTextArea(document.getElementById("editor"), {
      lineNumbers: true,
      mode: "text/x-vb",
      matchBrackets: true
    });
    ws = new WebSocket("ws://nado.oknctict.tk:5000/websock/ide/");
    session_id = null;
    ws.onclose = ws.onerror = function(error) {
      return alert("please reload web page");
    };
    ws.onmessage = function(event) {
      var msg;
      msg = event.data;
      console.log(msg);
      if (msg.command === "login_RES") {
        if (msg.data.result < 100) {
          session_id = msg.session_id;
          return $("#loginModal").modal("hide");
        } else {
          return $("#loginModal").modal("show");
        }
      }
    };
    make_msg = function(command, data) {
      var sid;
      if (session_id === null) {
        sid = "";
      } else {
        sid = session_id;
      }
      return JSON.stringify({
        type: "ide",
        session_id: sid,
        command: command + "_REQ",
        data: data
      });
    };
    $("#btn-login").click(function() {
      var msg, passwd, user_id;
      user_id = $("#user_id").val();
      passwd = $.sha256($("#passwd"));
      msg = make_msg("login", {
        user_id: user_id,
        password: passwd
      });
      console.log(msg);
      return ws.send(msg);
    });
    return $("#btn-upload").click(function() {
      if (session_id === null) {
        $("#loginModal").modal("show");
      }
    });
  });

}).call(this);
