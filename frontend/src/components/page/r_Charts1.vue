<template>
	<div>
		<!-- 面包屑导航 -->
		<div class="crumbs">
			<el-breadcrumb separator="/">
				<el-breadcrumb-item>
					<i class="el-icon-sunrise-1"></i> 光照图表
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
					<span class="label">光照开启时间</span>
					<el-badge :value="statue1.text" class="item" :type="statue1.type"></el-badge>
					<div class="slider-container">
						<el-input-number v-model="start" @change="set_light_on_time1" :min="0" :max="11"
							label="描述文字"></el-input-number>
					</div>
					<span class="label">光照关闭时间</span>
					<el-badge :value="statue2.text" class="item" :type="statue2.type"></el-badge>
					<div class="slider-container">
						<el-input-number v-model="end" @change="set_light_on_time2" :min="12" :max="23"
							label="描述文字"></el-input-number>
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
		r_SendLight
	} from '../../api/index.js';
	export default {
		name: 'Echarts1',
		data() {
			return {
				statue1: {
					text: '未更改',
					type: 'info',
				},
				statue2: {
					text: '未更改',
					type: 'info',
				},
				intensityData: [],
				start: 5,
				end: 21,
				light_time: {
					lighttime: 0,
					userid:0
				},
				option1: {
					title: {
						text: '过去24小时光照时长',
						left: 'center'
					},

					tooltip: {
						trigger: 'item'
					},
					legend: {
						orient: 'vertical',
						left: 'left'
					},
					series: [{
						
						type: 'pie',
						radius: '60%',
						data: [],
						emphasis: {
							itemStyle: {
								shadowBlur: 10,
								shadowOffsetX: 0,
								shadowColor: 'rgba(0, 0, 0, 0.5)'
							}
						}
					}]
				},
				myChart1: null,
			};
		},
		computed: {
		    
		},
		methods: {
			userid() {
			    let userid = localStorage.getItem('ms_userid');
				
				this.light_time.userid=userid;
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
			},
			rMoistureIntensityGet() {
				r_moisture_intensity_get().then(res => {
					let intensity1Count = 0;
					let intensity0Count = 0;
					for (const item of res) {
						if (item.intensity === 1) {
							intensity1Count++;
						} else if (item.intensity === 0) {
							intensity0Count++;
						}
					}

					this.intensityData = [{
							value: intensity1Count,
							name: '光照时长',
							itemStyle: {
								color: "#12df79"
							}
						},
						{
							value: intensity0Count,
							name: '黑暗时长',
							itemStyle: {
								color: "#04541d "
							}
						},
					];

					this.option1.series[0].data = this.intensityData;
					this.myEcharts();
				});
			},

			async set_light_on_time1() {
				try {
					this.light_time.lighttime = this.start;
					console.log(this.light_time)
					const response = await r_SendLight(this.light_time);
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
			async set_light_on_time2() {
				try {
					this.light_time.lighttime = this.end;
					
					const response = await r_SendLight(this.light_time);
					if (response.code == 200) {
						this.statue2.text = "成功";
						this.statue2.type = "success";
					} else {
						this.statue2.text = "失败";
						this.statue2.type = "warning";
					}
				} catch (error) {
					this.statue2.text = "失败";
					this.statue2.type = "warning";

				}
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