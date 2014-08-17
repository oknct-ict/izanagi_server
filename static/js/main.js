(function() {
  $(function() {
    var editor, event_handlers, make_msg, send, session_id, show_toast, ws;
    editor = CodeMirror.fromTextArea(document.getElementById("editor"), {
      lineNumbers: true,
      mode: "text/x-vb",
      matchBrackets: true
    });
    ws = new WebSocket("ws://nado.oknctict.tk:5000/websock/ide/");
    session_id = null;
    event_handlers = {};
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
    send = function(command, data, timeout) {
      var deferred, msg, timer_id;
      data || (data = {});
      timeout || (timeout = 5000);
      msg = make_msg(command, data);
      deferred = $.Deferred();
      timer_id = setTimeout(function() {
        return deferred.reject();
      }, timeout);
      event_handlers[command + "_RES"] = function(m) {
        deferred.resolve(m);
        return clearTimeout(timer_id);
      };
      ws.send(msg);
      console.log("Send:");
      console.log(msg);
      return deferred.promise();
    };
    show_toast = function(text) {
      var toast;
      toast = $('<div class="toast fade"><button type="button" class="close" data-dismiss="alert"></button><div class="toast-body"><p>' + text + '</p></div>');
      return $("#alerts-container").append(toast.addClass("in"));
    };
    ws.onerror = function(error) {
      return show_toast("please reload this web page");
    };
    ws.onmessage = function(event) {
      var msg;
      msg = JSON.parse(event.data);
      console.log("Receive:");
      console.log(msg);
      if (msg.command in event_handlers) {
        event_handlers[msg.command](msg);
      }
      return 0;
    };
    $("#projectModal").on("shown", function() {
      return send("pro_list", {}).then(function(msg) {
        return show_toast("pro_list passive");
      }, function() {});
    });
    $("#btn-login").click(function() {
      var passwd, user_id;
      user_id = $("#txt-login_user_id").val();
      passwd = $("#txt-login_passwd").val();
      return send("login", {
        user_id: user_id,
        password: passwd
      }).then(function(msg) {
        if (msg.data.result < 100) {
          session_id = msg.session_id;
          $("#loginModal").modal("hide");
        } else {
          session_id = null;
          show_toast("login failed");
        }
        return 0;
      }, function() {
        session_id = null;
        return show_toast("login timeout");
      });
    });
    return $("#btn-register").click(function() {
      var email, grade, passwd, passwd_confirm, school, user_id;
      user_id = $("#txt-register_user_id").val();
      passwd = $("#txt-register_passwd").val();
      passwd_confirm = $("#txt-register_passwd_confirm").val();
      email = $("#txt-register_email").val();
      school = parseInt($("#select-register_school").val());
      grade = parseInt($("#select-register_grade").val());
      if (passwd !== passwd_confirm) {
        show_toast("password incorrect");
        return 0;
      }
      return send("register", {
        user_id: user_id,
        password: passwd,
        address: email,
        grade: school * 10 + grade
      }).then(function(msg) {
        if (msg.data.result < 100) {
          session_id = msg.session_id;
          return $("#registerModal").modal("hide");
        } else {
          return show_toast("registration failed");
        }
      }, function() {
        return show_toast("registration timeout");
      });
    });
  });

}).call(this);
