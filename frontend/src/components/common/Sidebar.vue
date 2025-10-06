<template>
	<div class="sidebar">

		<el-menu class="sidebar-el-menu" :default-active="onRoutes" :collapse="collapse" background-color="#335735"
			text-color="#bfcbd9" active-text-color="#19bc63" unique-opened router>
			<template v-for="item in items">
				<template v-if="item.subs">
					<el-submenu class="menu-item" :index="item.index" :key="item.index">
						<template slot="title">
							<i :class="item.icon"></i>
							<span slot="title">{{ item.title }}</span>
						</template>
						<template v-for="subItem in item.subs">
							<el-submenu v-if="subItem.subs" :index="subItem.index" :key="subItem.index">
								<template slot="title">{{ subItem.title }}</template>
								<el-menu-item v-for="(threeItem,i) in subItem.subs" :key="i"
									:index="threeItem.index">{{ threeItem.title }}</el-menu-item>
							</el-submenu>
							<el-menu-item v-else :index="subItem.index"
								:key="subItem.index">{{ subItem.title }}</el-menu-item>
						</template>
					</el-submenu>
				</template>
				<template v-else>
					<el-menu-item class="menu-item" :index="item.index" :key="item.index">
						<i :class="item.icon"></i>
						<span slot="title">{{ item.title }}</span>
					</el-menu-item>
				</template>
			</template>
		</el-menu>

		<div v-if="!collapse" class="weather-component" :style="{ backgroundImage: `url(${weatherData.today_img})` }">
			<div class="weather-date">{{ weatherData.date }}</div>
			<div class="weather-date">重庆市-南岸区</div>
			<div class="weather-temp-now">{{ `${weatherData.today_temp_now}°` }}</div>
			<div class="weather-info">
				<img :src="weatherData.today_weather_img" class="weather-icon" />
				<div class="weather-description">{{ weatherData.today_weather }}</div>
			</div>
			<div class="weather-temp">{{ maxAndmin }}</div>
			<hr class="separator">
			<div class="weather-forecast">
				<div class="weather-forecast-text">

					<div>明天</div>
					<div>后天</div>
				</div>
				<div class="weather-forecast-description">

					<div>{{ weatherData.tom_weather }}</div>
					<div>{{ weatherData.after_weather }}</div>
				</div>
				<div class="weather-forecast-temp">

					<div>{{ weatherData.tom_temp }}</div>
					<div>{{ weatherData.after_temp }}</div>
				</div>
				<div class="weather-forecast-wind">

					<div>{{ weatherData.after_wind }}</div>
					<div>{{ weatherData.after_wind }}</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
	import bus from '../common/bus';
	import {
		r_weather_get
	} from '../../api/index.js'
	export default {
		data() {
			return {
				collapse: false,
				items: [{
						icon: 'el-icon-data-analysis',
						index: '3',
						title: '环境图表',
						subs: [

							{
								icon: 'el-icon-odometer',
								index: 'r_charts',
								title: '温度图表'
							},
							{
								icon: 'el-icon-sunrise-1',
								index: 'r_charts1',
								title: '光照图表'
							},
							{
								icon: 'el-icon-heavy-rain',
								index: 'r_charts2',
								title: '湿度图表'
							},
						]
					},
					{
						icon: 'el-icon-date',
						index: 'r_evopage',
						title: '历史数据'
					},
					{
						icon: 'el-icon-chat-dot-round',
						index: 'r_advise',
						title: '专家建议'
					},
					{
						icon: 'el-icon-lx-copy',
						index: 'r_tabs',
						title: '新闻视界'
					},
					{
						icon: 'el-icon-user',
						index: 'r_usermanagement',
						title: '用户管理'
					}
				],
				weatherData: {
					after_temp: "",
					after_weather: "",
					after_weather_img: "",
					after_wind: "",
					date: "",
					today_hum: "",
					today_temp: "",
					today_temp_now: "",
					today_weather: "",
					today_weather_img: "",
					today_wind: "",
					tom_temp: "",
					tom_weather: "",
					tom_weather_img: "",
					tom_wind: "",
					today_img: ""
				},
				maxAndmin: ''
			};
		},
		computed: {
			onRoutes() {
				return this.$route.path.replace('/', '');
			}
		},
		created() {
			// 通过 Event Bus 进行组件间通信，来折叠侧边栏
			bus.$on('collapse', msg => {
				this.collapse = msg;
				bus.$emit('collapse-content', msg);
			});
			this.getData();
			setInterval(this.getData, 600000)

		},
		methods: {
			getData() {
				r_weather_get().then(res => {
					this.weatherData = res[0];
					if (this.weatherData.today_temp) {
						this.formatTemperature(this.weatherData.today_temp);
					}
				});
			},
			formatTemperature(temperature) {
				const tempArr = temperature.split(' / ');
				const lowTemp = tempArr[0];
				const highTemp = tempArr[1];
				this.maxAndmin = `最低${lowTemp} 最高${highTemp}`;
			},
		},
	};
</script>

<style scoped>
	/* .menu-item {
	  height: 50px; 
	} */

	.sidebar {
		display: block;
		position: absolute;
		left: 0;
		top: 70px;
		bottom: 0;
		overflow-y: scroll;
	}

	.sidebar::-webkit-scrollbar {
		width: 0;
	}

	.sidebar-el-menu:not(.el-menu--collapse) {
		width: 250px;
	}

	.sidebar>ul {
		height: 100%;
	}

	.weather-component {
		color: #eaeaea;
		/* 设置字体颜色为白色 */
		padding: 10px;

		position: absolute;
		bottom: 10px;
		/* 调整与侧边栏的距离 */
		left: 20px;
		/* 调整与侧边栏的距离 */
		right: 20px;
		/* 调整与侧边栏的距离 */
		border-radius: 10px;
		/* 添加圆角边框 */
		background-size: cover;
		background-position: center;


	}

	.weather-info {
		display: flex;
		/* 使用 flex 布局 */
		align-items: center;
		margin-left: 52px;

		/* 垂直居中对齐 */

		/* 调整与 weather-temp 之间的间距 */
	}

	.weather-date {
		font-weight: bold;
		font-size: 18px;
		margin-bottom: 2px;
		display: flex;
		/* 使用 flex 布局 */
		justify-content: center;
		/* 水平居中对齐 */
	}

	.weather-temp-now {
		font-size: 50px;

		margin-bottom: -3px;
		/* 放大字体 */
		display: flex;
		/* 使用 flex 布局 */

		/* 水平居中对齐 */
		margin-left: 60px;
	}

	.weather-temp {
		display: flex;
		justify-content: center;
		font-size: 13px;
	}

	.weather-description {
		font-size: 13px;
	}

	.weather-icon {
		width: 45px;
		height: 45px;
	}


	.weather-forecast {
		display: flex;
		font-size: 10px;
		margin-bottom: -10px;
	}

	.weather-forecast>div {
		display: flex;
		flex-direction: column;
		justify-content: space-between;
	}

	.weather-forecast>div>div {
		margin-bottom: 5px;
		margin-right: 5px;
		margin-left: 5px;
	}

	.separator {
		border: none;
		height: 1px;
		margin: 5px 0;
		background: linear-gradient(to right, transparent, #ffffff, transparent);
	}
	.el-submenu-item, .el-submenu__title {
		height: 45px;
		line-height: 45px;
	}
	.el-menu-item, .el-submenu__title {
		height: 50px;
		line-height: 50px;
	}
</style>