<template>
	<div>
		<!-- 面包屑导航 -->
		<div class="crumbs">
			<el-breadcrumb separator="/">
				<el-breadcrumb-item><i class="el-icon-user"></i>用户管理</el-breadcrumb-item>
			</el-breadcrumb>
		</div>
		<div class="container">
			<span style="margin-left: 10px;">用户信息</span><el-button type="success" size="mini" @click="Enroll()" style="margin-left: 20px;">新增用户</el-button>
			<el-table stripe :data="tableData" style="width: 100%;margin: 10px;" height="240">
				<el-table-column label="用户名">
					<template slot-scope="scope">
						<span style="margin-left: 10px">{{ scope.row.username }}</span>
					</template>
				</el-table-column>
				<el-table-column label="用户ID">
					<template slot-scope="scope">
						<span>{{ scope.row.userid }}</span>
					</template>
				</el-table-column>
				<el-table-column label="密码">
					<template slot-scope="scope">
						<span>******</span>
					</template>
				</el-table-column>
				<el-table-column label="角色">
					<template slot-scope="scope">
						<span>{{ scope.row.role }}</span>
					</template>
				</el-table-column>
				<el-table-column label="操作">
					<template slot-scope="scope">
						<el-popconfirm @confirm="handleEdit(scope.$index, scope.row)" title="确定重置该用户吗？">
							<el-button style="margin-right: 10px;" size="mini" slot="reference">重置</el-button>
						</el-popconfirm>
						<el-popconfirm @confirm="handleDelete(scope.$index, scope.row)" title="确定删除该用户吗？">
							<el-button size="mini" type="danger" slot="reference">删除</el-button>
						</el-popconfirm>
					</template>
				</el-table-column>
			</el-table>
			<span style="margin-left: 10px;">用户操作记录</span>
			<el-table stripe :data="tableData2" style="width: 100%;margin: 10px;" height="240">
				<el-table-column label="序号">
					<template slot-scope="scope">
						<span style="margin-left: 10px">{{ scope.row.id }}</span>
					</template>
				</el-table-column>
				<el-table-column label="用户ID">
					<template slot-scope="scope">
						<span>{{ scope.row.userid }}</span>
					</template>
				</el-table-column>
				<el-table-column label="操作">
					<template slot-scope="scope">
						<span>{{ scope.row.operate }}</span>
					</template>
				</el-table-column>
				<el-table-column label="数值">
					<template slot-scope="scope">
						<span>{{ scope.row.value }}</span>
					</template>
				</el-table-column>
				<el-table-column label="时间">
					<template slot-scope="scope">
						<span>{{ scope.row.time }}</span>
					</template>
				</el-table-column>
			</el-table>
		</div>
	</div>
</template>

<script>
	import {
		r_GetAllUser
	} from '../../api/index.js'
	import {
		r_DeletUser
	} from '../../api/index.js'
	import {
		r_EditUser
	} from '../../api/index.js'
	import {
		r_GetOperationLog
	} from '../../api/index.js'
	export default {
		data() {
			return {
				tableData: [{
					role: '',
					userid: '',
					password: '',
					username: '',
				}],
				tableData2: [{
					id: '',
					userid: '',
					operate: '',
					value: '',
					time: '',
				}]
			}
		},
		created() {
			this.getData();
			//setInterval(this.getData, 5000);
		},
		methods: {
			Enroll(){
				this.$router.push('/enroll');
			},

			getData() {
				r_GetAllUser().then(res => {
					this.tableData = res.result;
				});
				r_GetOperationLog().then(res => {
					this.tableData2 = res.result;
				});
			},
			handleEdit(index, row) {
				row.password = '123456';
				r_EditUser(row).then(res => {
					if (res.code == 'success') {
						this.$message.success('重置成功!');
					} else {
						this.$message.error('重置失败');
					} // 处理响应结果
				});
			},
			handleDelete(index, row) {
				r_DeletUser(row).then(res => {
					console.log(res.code);
					if (res.code == 200) {
						this.$message.success('删除成功!');
					} else {
						this.$message.error('删除失败');
					}
					this.getData();
				});
			}
		}
	}
</script>

<style>
	.container {
		height: 530px;
	}
</style>