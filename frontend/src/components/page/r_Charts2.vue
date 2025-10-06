<template>
	<div>
		<!-- 面包屑导航 -->
		<div class="crumbs">
			<el-breadcrumb separator="/">
				<el-breadcrumb-item>
					<i class="el-icon-heavy-rain"></i> 湿度图表
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
					<span class="label">土壤湿度阈值</span>
					<el-badge :value="statue1.text" class="item" :type="statue1.type"></el-badge>
					<div class="slider-container">
						<el-slider v-model="moisture_gate.mois" :min="0" :max="100" :step="1" show-input
							@change="set_moisture_gate"></el-slider>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>


<script>
	import {
		r_moisture_intensity_get
	} from '../../api/index.js';
	import {
		setMoistureGate
	} from '../../api/index.js';
	import {
		r_GetMoisSet
	} from '../../api/index.js';
	export default {
		name: 'Echarts2',
		data() {
			return {
				statue1: {
					text: '未更改',
					type: 'info',
				},
				moisture_gate: {
					mois:0,
					userid:0
				},

				option1: {

					title: {
						text: '过去24小时大棚内土壤湿度与空气湿度',
						left: 'center'
					},
					tooltip: {
						trigger: 'axis',
						axisPointer: {
							animation: false
						}
					},
					legend: {
						data: ['土壤湿度', '空气湿度'],
						left: 10
					},

					axisPointer: {
						link: [{
							xAxisIndex: 'all'
						}]
					},

					grid: [{
							left: 60,
							right: 50,
							height: '30%'
						},
						{
							left: 60,
							right: 50,
							top: '55%',
							height: '30%'
						}
					],
					xAxis: [{
							type: 'category',
							boundaryGap: false,
							axisLine: {
								onZero: true
							},
							data: []
						},
						{
							gridIndex: 1,
							type: 'category',
							boundaryGap: false,
							axisLine: {
								onZero: true
							},
							data: [],
							position: 'top'
						}
					],
					yAxis: [{
							name: '空气湿度%',
							type: 'value',

						},
						{
							gridIndex: 1,
							name: '土壤湿度%',
							type: 'value',
							inverse: true
						}
					],
					series: [{
							name: '空气湿度',
							type: 'line',
							symbolSize: 8,
							// prettier-ignore
							data: [],
							smooth: true,
							showSymbol: false,
							areaStyle: {},
							animationEasing: "circularIn"
						},
						{
							name: '土壤湿度',
							type: 'line',
							xAxisIndex: 1,
							yAxisIndex: 1,
							symbolSize: 8,
							// prettier-ignore
							data: [],
							smooth: true,
							showSymbol: false,
							areaStyle: {},
							animationEasing: "circularIn"
						}
					]
				},
				myChart1: null,
			};
		},
		computed: {
		   
		},
		methods: {
			userid() {
			    let userid = localStorage.getItem('ms_userid');
				
				this.moisture_gate.userid=userid;
				return userid;
			},
			myEcharts() {
				if (this.myChart1 === null) {
					this.myChart1 = this.$echarts.init(document.getElementById('echart1'));
				}
				this.myChart1.setOption(this.option1);
			},
			getData() {
				this.rMoistureIntensityGet();
				this.GetMoisSet();
			},
			rMoistureIntensityGet() {
				r_moisture_intensity_get().then(res => {
					const currentHour = new Date().getHours();

					const timeData = [];
					for (let i = 0; i < 24; i++) {
						const hour = (currentHour - i + 24) % 24;
						const formattedHour = hour < 10 ? `0${hour}:00` : `${hour}:00`;
						timeData.unshift(formattedHour);
					}
					const moistureData = res.map(item => item.moisture);
					const humData = res.map(item => item.hum);

					this.option1.xAxis[0].data = timeData;
					this.option1.xAxis[1].data = timeData;
					this.option1.series[1].data = moistureData;
					this.option1.series[0].data = humData;

					this.myEcharts();
				});
			},

			async set_moisture_gate() {
				try {
					const response = await setMoistureGate(this.moisture_gate);
					if (response.code == 200) {
						this.statue1.text = "成功";
						this.statue1.type = "success";
					} else {
						this.statue1.text = "失败";
						this.statue1.type = "warning";
					}
				} catch (error) {
					this.statue1.text = "失败";
					this.statue1.type = "warning";

				}
			},
			GetMoisSet() {
				r_GetMoisSet().then(res => {
					this.moisture_gate.mois = res.tableData[0].moisture_set;
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
			this.userid();
			window.addEventListener('resize', this.handleResize);
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
		padding: 30px;
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