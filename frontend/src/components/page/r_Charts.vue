<template>
	<div>
		<!-- 面包屑导航 -->
		<div class="crumbs">
			<el-breadcrumb separator="/">
				<el-breadcrumb-item>
					<i class="el-icon-odometer"></i> 温度图表
				</el-breadcrumb-item>
			</el-breadcrumb>
		</div>
		<div class="container">
			<div class="charts">
				<!-- 图表容器 -->
				<div style="width:100%; height: 400px;" id="echart1"></div>
			</div>
			<div class="setTab">
				<!-- 数值设置面板 -->
				<div class="row">
					<span class="label">大棚温度阈值</span>
					<el-badge :value="statue.text" class="item" :type="statue.type"></el-badge>
					<div class="slider-container">
						<el-slider v-model="temp_gate.temp" :min="0" :max="50" :step="1" show-input
							@change="setTemp"></el-slider>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>


<script>
	import {
		setTempGate
	} from '../../api/index.js';
	import {
		r_GetTempSet
	} from '../../api/index.js';
	import {
		r_tempera_get
	} from '../../api/index.js';
	import {
		inside_tempera_get
	} from '../../api/index.js';
	export default {
		name: 'Echarts',
		data() {
			return {
				statue: {
					text: '未更改',
					type: 'info',
				},
				temp_gate: {
					temp: 0,
					userid: 0
				}, // 温度阈值设置
				option1: {
					title: {
						text: '前后6小时温度',
						left: "center",
					},
					tooltip: {
						trigger: 'axis'
					},
					legend: {
						show: true,
						right: "5%",

					},
					xAxis: {
						type: 'category',
						data: [],

						splitArea: {
							show: true
						}
					}, //X轴
					yAxis: {
						type: 'value',
						min: function(value) {
							return value.min - 3;
						},
						max: function(value) {
							return value.max + 3;
						},
						splitLine: {
							show: true
						},
						axisLabel: {
							formatter: '{value} °C'
						},
						axisLine: {
							show: false
						},
					}, //Y轴
					series: [{
							name: '外界气温',
							data: [],
							type: 'line',
							smooth: true,
							resize: true,
							markPoint: {
								data: [{
										type: 'max',
										name: 'Max'
									},
									{
										type: 'min',
										name: 'Min'
									}
								],
								symbolSize: 40
							},
							markLine: {
								data: [{
									type: 'average',
									name: 'ava'
								}],
								animationEasing: "bounceOut",

							},
							emphasis: {
								focus: 'series'
							},
						},
						{
							name: '大棚预测温度',
							data: [],
							type: 'line',
							smooth: true,
							resize: true,
							markPoint: {
								data: [{
										type: 'max',
										name: 'Max'
									},
									{
										type: 'min',
										name: 'Min'
									}
								],
								symbolSize: 40
							},
							markLine: {
								data: [{
									type: 'average',
									name: 'ava'
								}],
								animationEasing: "bounceOut",

							},
							emphasis: {
								focus: 'series'
							},
							lineStyle: {
								type: "dotted"
							}
						},
						{
							name: '大棚温度',
							data: [],
							type: 'line',
							smooth: true,
							resize: true,
							markPoint: {
								data: [{
										type: 'max',
										name: 'Max'
									},
									{
										type: 'min',
										name: 'Min'
									}
								],
								symbolSize: 40
							},
							markLine: {
								data: [{
									type: 'average',
									name: 'ava'
								}],
								animationEasing: "bounceOut",

							},
							emphasis: {
								focus: 'series'
							},

						},
					] //配置项
				},
				myChart1: null,
			};
		},
		computed: {

		},
		methods: {
			userid() {
				let userid = localStorage.getItem('ms_userid');
				console.log(userid);
				this.temp_gate.userid = userid;

			},
			myEcharts() {
				if (this.myChart1 === null) {
					this.myChart1 = this.$echarts.init(document.getElementById('echart1'));
				}
				this.myChart1.setOption(this.option1);
			},
			getData() {
				this.rTemperaGet();
				this.insideTemperaGet();
				this.getTempSet();
			},
			rTemperaGet() {
				r_tempera_get().then(res => {
					const data = res;
					const currentTime = new Date().getHours();
					const times = [];
					const temps = [];
					const pre_temp = [];

					for (let i = currentTime - 6; i <= currentTime + 6; i++) {
						const normalizedTime = (i + 24) % 24;
						const matchingData = data.find(item => item.time === normalizedTime);

						if (matchingData) {
							const formattedTime = `${normalizedTime}:00`;
							times.push(formattedTime);
							temps.push(matchingData.temp);
							pre_temp.push(matchingData.pre_temp);
						}
					}

					this.option1.xAxis.data = times;
					this.option1.series[0].data = temps;
					this.option1.series[1].data = pre_temp;

					this.myEcharts();
				});
			},
			insideTemperaGet() {
				inside_tempera_get().then(res => {
					const data = res;
					const currentTime = new Date().getHours();
					const times = [];
					const inside_temp = [];

					for (let i = currentTime - 6; i <= currentTime + 6; i++) {
						const normalizedTime = (i + 24) % 24;
						const matchingData = data.find(item => item.time === normalizedTime);

						if (matchingData) {
							const formattedTime = `${normalizedTime}:00`;
							times.push(formattedTime);
							inside_temp.push(matchingData.inside_temp);
						}
					}

					this.option1.xAxis.data = times;
					this.option1.series[2].data = inside_temp;

					this.myEcharts();
				});
			},
			async setTemp() {
				try {
					const response = await setTempGate(this.temp_gate);
					if (response.code == 200) {
						this.statue.text = "成功";
						this.statue.type = "success";
					} else {
						this.statue.text = "失败";
						this.statue.type = "warning";
					}
				} catch (error) {
					this.statue.text = "失败";
					this.statue.type = "warning";

				}
			},
			getTempSet() {
				r_GetTempSet().then(res => {
					this.temp_gate.temp = res.tableData[0].temp_set;
				});
			},
			handleResize() {
				// 监听窗口大小变化事件，并重新设置图表容器的宽度和高度
				if (this.myChart1) {
					this.myChart1.resize();
				}
			},
		},
		mounted() {
			this.myEcharts();
			this.getData();
			setInterval(this.getData, 3600000);
			window.addEventListener('resize', this.handleResize);
			this.userid();
		},
		beforeDestroy() {
			window.removeEventListener('resize', this.handleResize);
		},
	}
</script>

<style>
	.item {
		margin-right: 10px;
		margin-top: 3px;
	}

	.content-title {
		clear: both;
		font-weight: 400;
		line-height: 50px;
		margin: 10px 0;
		font-size: 22px;
		color: #1f2f3d;
	}

	.setTab {
		margin-top: 20px;
		padding: 20px;
	}

	.row {
		display: flex;
		align-items: center;
	}

	.label {
		margin-right: 10px;
	}

	.slider-container {
		flex-grow: 1;
	}
</style>