if ngx.var.arg_ch == nil then
   ngx.log(ngx.ERR, "request uri is not found channel is null")
   return 404
end

local channel = ngx.var.arg_ch
local ptools = require "pubTools"
local date, time = ptools.get_curDateTime()
--根据channel来判读当前是否有直播的内容；
local command = ("select media_url from program where channel_id = "..channel.." and media_type = 'live' and status = 'normal' and lv_date = "..date.." and start_time <= "..time.." and end_time>="..time.." limit 1")
ngx.log(ngx.ERR,"command is ", command)
local mySql = require "myExc"
local res = mySql.query(command)

ngx.log(ngx.ERR,"command is ", res["medis_url"])
local m3u8List = ptools.getM3u8List(res["media_url"])

ngx.log(ngx.ERR, m3u8List)

-- get data from shared dict and put them into mysql
--local key = "logs"
--local vals = ""
--local temp_val = ngx.shared.logs:lpop(key)
--while (temp_val ~= nil)
--do
    --vals = vals .. ",".. temp_val
    --temp_val = ngx.shared.logs:lpop(key)
--end

--if vals ~= "" then
    --vals = string.sub(vals, 2,-1)
    --local command = ("insert into es_visit_record(access_ip,server_ip,access_time,run_time,es_response_time,request_body_byte,run_state,url,post_data) values "..vals)
    --ngx.log(ngx.ERR,"command is ",command)
    --local res, err, errcode, sqlstate = db:query(command)
    --if not res then
        --ngx.log(ngx.ERR,"insert error: ", err, ": ", errcode, ": ", sqlstate, ".")
        --return
    --end
--end
