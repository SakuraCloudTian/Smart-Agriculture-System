import request from '../utils/request';

export const fetchData = query => {
	return request({
		url: './table.json',
		method: 'post',
		params: query
	});
};
/**
 method of Login 
 
export const LoginInfo = parms => {
    return request({
        url: 'http://127.0.0.1:4523/m1/2368747-0-default/LoginInfo',
        method: 'get',
        params: parms
    });
};
*/
export const Chart1 = () => {
	return request({
		url: 'http://127.0.0.1:4523/m1/2368747-0-default/Chart1',
		method: 'get'

	});
};
/*
export const Table2 = pa => {
    return request({
        url: 'http://192.168.1.54:9091/api/loginPost',
        method: 'post',
		data: pa
    });
};
*/
//迭代1所用的接口如下
export const r_LoginInfo = parms1 => {
	return request({
		url: 'http://192.168.1.54:9091/api/r_LoginInfo',
		method: 'post',
		data: parms1
	});
};
export const r_Chart1 = () => {
	return request({
		url: 'http://192.168.1.54:9091/api/r_Chart1',
		method: 'get',

	});
};
export const r_EnvironmentInfo = () => {
	return request({
		url: 'http://192.168.1.54:9091/api/r_EnvironmentInfo',
		method: 'get',

	});
};
export const setFan = fan_temp => {
	return request({
		url: 'http://192.168.1.54:9091/api/r_FanAdjustment',
		method: 'post',
		data: {
			fan_setting: fan_temp
		}
	});
};
export const setPump = pump_temp => {
	return request({
		url: 'http://192.168.1.54:9091/api/r_AdjustWater',
		method: 'post',
		data: {
			water: pump_temp
		}
	});
};
export const setMoistureGate = MoistureGate_temp => {
	return request({
		url: 'http://192.168.1.54:9091/api/r_AdjustMois',
		method: 'post',
		data: MoistureGate_temp
	});
};
export const r_ReturnNews = () => {
	return request({
		url: 'http://192.168.1.54:9091/api/r_ReturnNews',
		method: 'get',

	});
};
export const getnews = parms2 => {
	return request({
		url: 'http://192.168.1.54:9091/api/getnews',
		method: 'get',
		params: parms2

	});
};
export const enrollInfo = enrollData => {
	return request({
		url: 'http://192.168.1.54:9091/api/r_Register',
		method: 'post',
		data: enrollData
	});
};
export const r_GetAvergeTemp = () => {
	return request({
		url: 'http://192.168.1.54:9091/api/r_GetAvergeTemp',
		method: 'get',

	});
};
export const r_GetAvergeHum = () => {
	return request({
		url: 'http://192.168.1.54:9091/api/r_GetAvergeHum',
		method: 'get',

	});
};
export const r_GetAvergeMoist = () => {
	return request({
		url: 'http://192.168.1.54:9091/api/r_GetAvergeMoist',
		method: 'get',

	});
};
export const r_GetAverMois = () => {
	return request({
		url: 'http://192.168.1.54:9091/api/r_GetAverMois',
		method: 'get',

	});
};
export const r_AdjustLight = light_temp => {
	return request({
		url: 'http://192.168.1.54:9091/api/r_AdjustLight',
		method: 'post',
		data: light_temp


	});
};
export const r_WatertInfo = () => {
	return request({
		url: 'http://192.168.1.54:9091/api/r_WatertInfo',
		method: 'get'
	});
};
export const setTempGate = temp_temp => {
	return request({
		url: 'http://192.168.1.54:9091/api/r_TempAdjustment',
		method: 'post',
		data: temp_temp

	});
};
export const r_tempera_get = () => {
	return request({
		url: 'http://farmcontrol.natapp1.cc/api/tempera_get',
		method: 'get',
	});
};
export const inside_tempera_get = () => {
	return request({
		url: 'http://farmcontrol.natapp1.cc/api/inside_tempera_get',
		method: 'get',
	});
};
export const r_weather_get = () => {
	return request({
		url: 'http://farmcontrol.natapp1.cc/api/get_weather',
		method: 'get',
	});
};
export const r_GetTempSet = () => {
	return request({
		url: 'http://192.168.1.54:9091/api/r_GetTempSet',
		method: 'get',
	});
};
export const r_moisture_intensity_get = () => {
	return request({
		url: 'http://farmcontrol.natapp1.cc/api/moisture_intensity_get',
		method: 'get',
	});
};
export const r_SendLight = Light_temp => {
	return request({
		url: 'http://192.168.1.54:9091/api/r_SendLight',
		method: 'post',
		data: Light_temp
	});
};
export const r_GetMoisSet = () => {
	return request({
		url: 'http://192.168.1.54:9091/api/r_GetMoisSet',
		method: 'get',
	});
};
export const r_GetAdvise = () => {
	return request({
		url: 'http://192.168.1.54:9091/api/r_GetSuggestion',
		method: 'get',
	});
};
export const r_PublishSuggestion = Suggestion => {
	return request({
		url: 'http://192.168.1.54:9091/api/r_PublishSuggestion',
		method: 'post',
		data: Suggestion
	});
};
export const r_SelectByTime = date => {
	return request({
		url: 'http://192.168.1.54:9091/api/r_SelectByTime',
		method: 'get',
		params: date
	});
};
export const r_SelectByTime2 = date => {
	return request({
		url: 'http://192.168.1.54:9091/api/r_SelectByTime2',
		method: 'get',
		params: date
	});
};
export const r_GetAllUser = () => {
	return request({
		url: 'http://192.168.1.54:9091/api/r_GetAllUser',
		method: 'get',
	});
};
export const r_DeletUser = userid => {
	return request({
		url: 'http://192.168.1.54:9091/api/r_DeletUser',
		method: 'get',
		params: userid
	});
};
export const r_EditUser = user => {
	return request({
		url: 'http://192.168.1.54:9091/api/r_EditUser',
		method: 'post',
		data: user
	});
};
export const r_GetOperationLog =() => {
	return request({
		url: 'http://192.168.1.54:9091/api/r_GetOperationLog',
		method: 'get',
	});
};