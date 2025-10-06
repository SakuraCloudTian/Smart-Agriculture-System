<template>
	<div >
		<!-- 面包屑导航 -->
		<div class="crumbs">
			<el-breadcrumb separator="/">
				<el-breadcrumb-item><i class="el-icon-date"></i>历史数据</el-breadcrumb-item>
			</el-breadcrumb>
		</div>
		<div class="container">
			<!-- 刷新按钮 -->
			<div class="header_search">
				<div class="block">
					<el-date-picker @change="fresh()" v-model="time_value" type="date" placeholder="选择日期"
						:picker-options="pickerOptions">
					</el-date-picker>
				</div>
				

			</div>
			<div>
				<el-row :gutter="20">
					<el-col :span='12'>
						<!-- 表格(空气湿度,温度,光照,风扇) -->

						<el-table :data="tableData" style="" height="450px">
							<el-table-column prop="time" label="时间" width="180"></el-table-column>
							<el-table-column prop="temp" label="温度 单位:℃"></el-table-column>
							<el-table-column prop="hum" label="湿度"></el-table-column>
							<el-table-column prop="light_level" label="光照强度"></el-table-column>
							<el-table-column prop="fanlevel" label="风扇风力等级"></el-table-column>
						</el-table>

					</el-col>
					<el-col :span='12'>
						<!-- 表格(土壤湿度,水泵强度) -->
						<el-table :data="mosData" style="" height="450px">
							<el-table-column prop="time" label="时间" width="180"></el-table-column>
							<el-table-column prop="moisture" label="土壤湿度"></el-table-column>
							<el-table-column prop="water_pump_level" label="水泵强度"></el-table-column>
						</el-table>

					</el-col>
				</el-row>
			</div>
		</div>
	</div>
</template>

<script>
	import {
		r_SelectByTime
	} from '../../api/index.js'
	import {
		r_SelectByTime2
	} from '../../api/index.js'

	export default {
		data() {
			return {
				pickerOptions: {
					disabledDate(time) {
						return time.getTime() > Date.now();
					},
					shortcuts: [{
						text: '今天',
						onClick(picker) {
							picker.$emit('pick', new Date());
						}
					}, {
						text: '昨天',
						onClick(picker) {
							const date = new Date();
							date.setTime(date.getTime() - 3600 * 1000 * 24);
							picker.$emit('pick', date);
						}
					}, {
						text: '一周前',
						onClick(picker) {
							const date = new Date();
							date.setTime(date.getTime() - 3600 * 1000 * 24 * 7);
							picker.$emit('pick', date);
						}
					}]
				},
				time_value: Date.now(),
				date: {
					Year: '',
					Month: '',
					Day: ''
				},

				tableData: [{ // 表格1的数据
					temp: '1',
					hum: '1',
					light_level: '1',
					time: '1900-00-10 00:00:00',
					fanlevel: '1'
				}],

				mosData: [{ // 表格2的数据
					time: '1900-00-10 00:00:00',
					moisture: '1',
					water_pump_level: '1'
				}]
			}
		},
		created() {
			this.getData();

			//setInterval(this.getData, 5000);
		},
		computed: {

		},
		methods: {


			// 获取环境数据和水泵数据
			getData() {
				const timestamp = this.time_value;
				const date = new Date(timestamp);
				this.date.Year = date.getFullYear().toString();
				this.date.Month = (date.getMonth() + 1).toString().padStart(2, "0");
				this.date.Day = date.getDate().toString().padStart(2, "0");
				console.log(this.date)

				r_SelectByTime(this.date).then(res => {
					this.tableData = res.result;
				});
				r_SelectByTime2(this.date).then(res => {
					this.mosData = res.result;
				});
			},

			// 刷新数据
			fresh() {
				this.getData();
			},
		}
	}
</script>

<style scoped>
	

	.container {
		padding: 20px;
	}

	.table1 {
		margin-bottom: 20px;
	}

	.table2 {
		margin-bottom: 20px;
	}
	.header_search {
		display: flex;
		align-items: center;
		margin-bottom: 20px;
	}
</style>