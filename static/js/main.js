(function() {
  $(function() {
    var IzanagiConnection, IzanagiWebSocket, User, con, editor, showToast;
    editor = CodeMirror.fromTextArea(document.getElementById("editor"), {
      lineNumbers: true,
      mode: "text/x-vb",
      matchBrackets: true
    });
    showToast = function(text) {
      var toast;
      toast = $('<div class="toast fade"><button type="button" class="close" data-dismiss="alert"></button><div class="toast-body"><p>' + text + '</p></div>');
      return $("#alerts-container").append(toast.addClass("in"));
    };
    User = (function() {
      function User(userId, sessionId) {
        if (userId == null) {
          userId = null;
        }
        if (sessionId == null) {
          sessionId = null;
        }
        this._userId = userId;
        this._sessionId = sessionId;
      }

      User.prototype.setUser = function(userId, sessionId) {
        if (userId === null) {
          if (this._userId !== null) {
            this.onLogout(this._userId, this._sessionId);
          }
          this._userId = userId;
          return this._sessionId = sessionId;
        } else if (userId !== this._userId) {
          if (this._userId !== null) {
            this.onLogout(this._userId, this._sessionId);
          }
          this.onLogin(userId, sessionId);
          this._userId = userId;
          return this._sessionId = sessionId;
        } else {
          return this._sessionId = sessionId;
        }
      };

      User.prototype.onLogout = function() {
        return 0;
      };

      User.prototype.onLogin = function() {
        return 0;
      };

      return User;

    })();
    IzanagiWebSocket = (function() {
      IzanagiWebSocket.SERVER_URL = "ws://nado.oknctict.tk:5000/websock/ide/";

      function IzanagiWebSocket(receiver, error) {
        receiver || (receiver = function() {
          return 0;
        });
        error || (error = function() {
          return 0;
        });
        this._websocket = new WebSocket(IzanagiWebSocket.SERVER_URL);
        this._websocket.onerror = error;
        this._websocket.onmessage = function(event) {
          return receiver(JSON.parse(event.data));
        };
      }

      IzanagiWebSocket.prototype.sendJSON = function(data) {
        return this._websocket.send(JSON.stringify(data));
      };

      return IzanagiWebSocket;

    })();
    IzanagiConnection = (function() {
      IzanagiConnection.CONNECTION_TYPE = "ide";

      IzanagiConnection.DEFAULT_TIMEOUT = 5000;

      IzanagiConnection.ERROR_TIMEOUT = -1;

      function IzanagiConnection() {
        this._user = new User();
        this._eventHandlers = {};
        this._izanagiWebSocket = new IzanagiWebSocket((function(_this) {
          return function(msg) {
            if (msg.command in _this._eventHandlers) {
              _this._eventHandlers[msg.command](msg);
              delete _this._eventHandlers[msg.command];
            }
            return 0;
          };
        })(this), function() {
          return showToast("please reload this web page");
        });
        this._validResponse = function(msg) {
          return msg.data.result < 100;
        };
        this._makePacket = function(command, data) {
          var sid;
          if (this._user._sessionId === null) {
            sid = "";
          } else {
            sid = this._user._sessionId;
          }
          return {
            type: IzanagiConnection.CONNECTION_TYPE,
            session_id: sid,
            command: command + "_REQ",
            data: data
          };
        };
        this._sendCommand = function(command, data, timeout) {
          var deferred, timerId;
          if (data == null) {
            data = {};
          }
          if (timeout == null) {
            timeout = IzanagiConnection.DEFAULT_TIMEOUT;
          }
          deferred = $.Deferred();
          timerId = setTimeout(function() {
            return deferred.reject(IzanagiConnection.ERROR_TIMEOUT);
          }, timeout);
          this._eventHandlers[command + "_RES"] = (function(_this) {
            return function(m) {
              if (_this._validResponse(m)) {
                deferred.resolve(m);
              } else {
                deferred.reject(m.data.result);
              }
              return clearTimeout(timerId);
            };
          })(this);
          this._izanagiWebSocket.sendJSON(this._makePacket(command, data));
          return deferred.promise();
        };
        0;
      }

      IzanagiConnection.prototype.login = function(userId, password) {
        return this._sendCommand("login", {
          user_id: userId,
          password: password
        }).done((function(_this) {
          return function(msg) {
            return _this._user.setUser(userId, msg.session_id);
          };
        })(this)).fail((function(_this) {
          return function(error) {
            return _this._user.setUser(null, null);
          };
        })(this));
      };

      IzanagiConnection.prototype.register = function(userId, password, email, grade) {
        return this._sendCommand("register", {
          user_id: userId,
          password: password,
          address: email,
          grade: grade
        }).done((function(_this) {
          return function(msg) {
            return _this._user.setUser(userId, msg.session_id);
          };
        })(this)).fail((function(_this) {
          return function(error) {
            return _this._user.setUser(null, null);
          };
        })(this));
      };

      IzanagiConnection.prototype.getProjects = function() {
        return this._sendCommand("pro_list", {});
      };

      IzanagiConnection.prototype.createProject = function(projectName) {
        return this._sendCommand("pro_create", {
          project_name: projectName
        });
      };

      IzanagiConnection.prototype.renameProject = function(projectId, projectName) {
        return this._sendCommand("pro_rename", {
          project_id: projectId,
          project_name: projectName
        });
      };

      IzanagiConnection.prototype.deleteProject = function(projectId) {
        return this._sendCommand("pro_delete", {
          project_id: projectId
        });
      };

      IzanagiConnection.prototype.saveFile = function(projectId, dirName, fileName, code) {
        return this._sendCommand("save", {
          file_name: fileName,
          project_id: projectId,
          dir: dirName,
          code: code
        });
      };

      IzanagiConnection.prototype.updateFile = function(fileId, code) {
        return this._sendCommand("renew", {
          file_id: fileId,
          code: code
        });
      };

      IzanagiConnection.prototype.openFile = function(fileId) {
        return this._sendCommand("open", {
          file_id: fileId
        });
      };

      IzanagiConnection.prototype.deleteFile = function(fileId) {
        return this._sendCommand("delete", {
          file_id: fileId
        });
      };

      IzanagiConnection.prototype.setOnLogin = function(handler) {
        return this._user.onLogin = handler;
      };

      IzanagiConnection.prototype.setOnLogout = function(handler) {
        return this._user.onLogout = handler;
      };

      return IzanagiConnection;

    })();
    con = new IzanagiConnection();
    con.setOnLogin(function(userId, sessionId) {
      showToast("Welcome " + userId);
      $("#icon-btn_register").addClass("disable");
      $("#icon-btn_login").addClass("disable");
      return $("#icon-btn_project").removeClass("disable");
    });
    con.setOnLogout(function(userId, sessionId) {
      showToast("Bye " + userId);
      $("#icon-btn_register").removeClass("disable");
      $("#icon-btn_login").removeClass("disable");
      return $("#icon-btn-project").addClass("disable");
    });
    $("#projectModal").on("shown", function() {
      return con.getProjects().done(function() {});
    });
    $("#btn-login").click(function() {
      var password, userId;
      userId = $("#txt-login_user_id").val();
      password = $("#txt-login_passwd").val();
      return con.login(userId, password).done(function() {
        return $("#loginModal").modal("hide");
      }).fail(function() {
        return showToast("login failed");
      });
    });
    return $("#btn-register").click(function() {
      var email, grade, password, passwordConfirm, school, userId;
      userId = $("#txt-register_user_id").val();
      password = $("#txt-register_passwd").val();
      passwordConfirm = $("#txt-register_passwd_confirm").val();
      email = $("#txt-register_email").val();
      school = parseInt($("#select-register_school").val());
      grade = parseInt($("#select-register_grade").val());
      if (password !== passwordConfirm) {
        showToast("password incorrect");
        return 0;
      }
      return con.register(userId, password, email, school * 10 + grade).done(function() {
        return $("#registerModal").modal("hide");
      }).fail(function() {
        return showToast("registration failed");
      });
    });
  });

}).call(this);
