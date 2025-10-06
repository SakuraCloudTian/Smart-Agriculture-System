<template>
	<div>
		<div class="crumbs">
			<!-- 页眉小标题 -->
			<el-breadcrumb separator="/">
				<el-breadcrumb-item><i class="el-icon-chat-dot-round"></i>专家建议</el-breadcrumb-item>
			</el-breadcrumb>
		</div>
		<div class="container">

			<!-- 输入框 -->
			<div style="margin-bottom: 10px;">专家建议</div>
			<div style="margin-bottom: 10px;">
				<el-input type="textarea" :rows="5" placeholder="请输入建议" v-model="textarea.suggestion">
				</el-input>
			</div>
			<div style="margin-bottom: 10px;display: flex;justify-content: center;"><el-button type="success"
					style="" @click="postSuggestion">发布</el-button>
			</div>

			<el-tabs v-model="message">
				<el-tab-pane :label="`已发布建议(${sent.length})`" name="first">
					<el-table :data="sent" :show-header="false" style="width: 100%">
						<el-table-column>
							<template slot-scope="scope">
								<span class="">{{scope.row.suggestion}}</span>
							</template>
						</el-table-column>
						<el-table-column fixed="right" width="200px">
							<template slot-scope="scope">
								<span class="">{{scope.row.time}}</span>
							</template>
						</el-table-column>
					</el-table>
				</el-tab-pane>

			</el-tabs>
		</div>
		<!-- 建议详情对话框 -->
	</div>
</template>

<script>
	import {
		r_GetAdvise
	} from '../../api/index.js'
	import {
		r_PublishSuggestion
	} from '../../api/index.js'
	export default {
		name: 'tabs',
		data: function() {
			return {
				textarea: {
					suggestion:'',
					userid:0
				},
				message: 'first',
				sent: [{
					time: null,
					suggestion: null,
					
				}],
			}
		},
		created() {
			this.getData();
			this.userid();
		},
		methods: {
			userid() {
			    let userid = localStorage.getItem('ms_userid');
				console.log(userid);
				this.textarea.userid=userid;
				
			},
			// 获取数据
			getData() {
				r_GetAdvise().then(res => {
					this.sent = res.result;
				});
			},
			postSuggestion(){
				if(this.textarea.suggestion!=''){
				r_PublishSuggestion(this.textarea).then(res => {
						if (res.code == 200) {
							this.textarea.suggestion=null;
							this.getData();
							this.$message.success('发布成功(￣▽￣)／');
						} else {
							this.$message.error('发布失败╮(╯﹏╰）╭');
							return false;
						}
					});
					}
				else{
					this.$message.error('内容不能为空ヽ(`Д´)ﾉ');
				}
			}
		},
		computed: {

		}
	}
</script>

<style>
	.handle-row {
		margin-top: 30px;
	}

	.login-btn {
		margin-top: 30px;
	}
</style>