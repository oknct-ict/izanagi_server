(function() {
  $(function() {
    var IzanagiConnection, IzanagiWebSocket, Project, User, con, editor, showToast;
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
    Project = (function() {
      function Project(projectId, projectName) {
        this.projectId = projectId;
        this.projectName = projectName;
        0;
      }

      Project.create = function(projectName) {};

      return Project;

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
      User = (function() {
        function User(_userId, _sessionId) {
          this._userId = _userId != null ? _userId : null;
          this._sessionId = _sessionId != null ? _sessionId : null;
        }

        User.prototype.setUser = function(userId, sessionId) {
          if (this._userId !== null) {
            this.onLogout(this._userId, this._sessionId);
          }
          if (userId !== null) {
            this.onLogin(userId, sessionId);
          }
          this._userId = userId;
          return this._sessionId = sessionId;
        };

        User.prototype.onLogout = function() {};

        User.prototype.onLogin = function() {};

        return User;

      })();

      Project = (function() {
        Project.STATE_READY = 0;

        Project.STATE_CREATING = 1;

        Project.STATE_RENAMING = 2;

        Project.STATE_DELETING = 3;

        Project.STATE_EMPTY = 4;

        Project.ERROR_ALREADY_EXISTS = -2;

        function Project(projectName, projectId) {
          this.projectName = projectName != null ? projectName : "";
          this.projectId = projectId != null ? projectId : null;
          if (this.projectId === null) {
            this.state = Project.STATE_EMPTY;
          } else {
            this.state = Project.STATE_READY;
          }
        }

        Project.prototype.create = function(conn) {
          var deferred;
          if (this.state === Project.STATE_READY) {
            deferred = $.Deferred();
            deferred.reject(Project.ERROR_ALREADY_EXISTS);
            return deferred.promise();
          } else {
            this.state = Project.STATE_CREATING;
            return conn._sendCommand("pro_create", {
              project_name: this.projectName
            }).done((function(_this) {
              return function(msg) {
                _this.projectId = msg.data.project_id;
                return _this.state = Project.STATE_READY;
              };
            })(this));
          }
        };

        Project.prototype.rename = function(conn, projectName) {
          this.state = Project.STATE_RENAMING;
          return conn._sendCommand("pro_rename", {
            project_id: this.projectId,
            project_name: projectName
          }).done((function(_this) {
            return function(msg) {
              _this.projectName = projectName;
              return _this.state = Project.STATE_READY;
            };
          })(this)).fail((function(_this) {
            return function() {
              return _this.state = Project.STATE_READY;
            };
          })(this));
        };

        Project.prototype["delete"] = function(conn) {
          this.state = Project.STATE_DELETING;
          return conn._sendCommand("pro_delete", {
            project_id: this.projectId
          }).done((function(_this) {
            return function(msg) {
              _this.projectName = "";
              _this.projectId = null;
              return _this.state = Project.STATE_EMPTY;
            };
          })(this)).fail((function(_this) {
            return function() {
              return _this.state = Project.STATE_EMPTY;
            };
          })(this));
        };

        return Project;

      })();

      IzanagiConnection.CONNECTION_TYPE = "ide";

      IzanagiConnection.DEFAULT_TIMEOUT = 5000;

      IzanagiConnection.ERROR_TIMEOUT = -1;

      IzanagiConnection.MAX_REQUEST_ID = 10000;

      function IzanagiConnection() {
        this._requestId = 0;
        this._user = new User();
        this._eventHandlers = {};
        this._izanagiWebSocket = new IzanagiWebSocket((function(_this) {
          return function(msg) {
            if (msg.request_id in _this._eventHandlers) {
              _this._eventHandlers[msg.request_id](msg);
              delete _this._eventHandlers[msg.request_id];
            }
            return 0;
          };
        })(this), function() {
          return showToast("please reload this web page");
        });
        this._validResponse = function(msg, command) {
          return msg.data.result < 100 && msg.command === command + "_RES";
        };
        this._makePacket = function(command, data) {
          var rid, sid;
          rid = this._requestId;
          this._requestId = (this._requestId + 1) % IzanagiConnection.MAX_REQUEST_ID;
          if (this._user._sessionId === null) {
            sid = "";
          } else {
            sid = this._user._sessionId;
          }
          return {
            type: IzanagiConnection.CONNECTION_TYPE,
            session_id: sid,
            command: command + "_REQ",
            request_id: rid,
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
          this._eventHandlers[this._requestId] = (function(_this) {
            return function(m) {
              if (_this._validResponse(m, command)) {
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
