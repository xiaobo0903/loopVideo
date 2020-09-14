--mysql数据库的查询程序；
local connectMysqlUtil = {}

local mysql = require "resty.mysql"
-- connect to mysql;
function connectMysqlUtil.connect()
    local db, err = mysql:new()
    if not db then
        return false
    end
    db:set_timeout(1000)
    
    local ok, err, errno, sqlstate = db:connect{
        host = "127.0.0.1",
        port = 3306,
        database = "loopvideo",
        user = "root",
        password = "mysql",
        charset = "utf8",
        max_packet_size = 1024 * 1024 }
    
    if not ok then
    ngx.say("connect mysql failed")
        return false
    end
    return db
end
function connectMysqlUtil.query(command)

    local db = connectMysqlUtil.connect()
    if not db then
        ngx.say("the mysql database connect is error!")
        return nil
    end
    local res, err, errcode, sqlstate =
        db:query(command)
    if not res then
        ngx.say("bad result: ", err, ": ", errcode, ": ", sqlstate, ".")
        return nil
    end
    return res
end
return connectMysqlUtil
