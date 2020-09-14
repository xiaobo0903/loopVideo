--系统的公共工具集内容;
http = require("socket.http")

local _M = {}
--获取当前时间的日期与时间，都是数字格式，如20200101 010101等
function _M.get_curDateTime()

    dt = os.date("%Y%m%d %H%M%S", os.time())
    input = tostring(dt)
    -- for each divider found
    pos = string.find(input, ' ', 0, true)

    date = string.sub(input, 0, pos-1)

    time = string.sub(input, pos)
    ngx.log(ngx.ERR, "1111111", date, time)
    return date, time
end
--获取m3u8文件的列表内容，其中即包含直播的m3u8也包括点播的内容；
function _M.getM3u8List(url)
    ret = http.request(url);
    ngx.log(ngx.ERR, ret)
end
return _M
