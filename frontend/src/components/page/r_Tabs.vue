<template>
	<div>
		<div class="crumbs">
			<!-- 页眉小标题 -->
			<el-breadcrumb separator="/">
				<el-breadcrumb-item><i class="el-icon-lx-copy"></i>新闻视界</el-breadcrumb-item>
			</el-breadcrumb>
		</div>
		<div class="container">
			<div style="margin-top: 10px;margin-bottom: 10px;" v-model="input">
				<!-- 搜索框 -->
				<el-input @keyup.enter.native="search()" placeholder="请输入内容" v-model="input" class="input-with-select">
					<el-select v-model="select" slot="prepend" placeholder="请选择">
						<el-option label="标题" value="title"></el-option>
						<el-option label="内容" value="content"></el-option>
						<el-option label="作者" value="author"></el-option>
					</el-select>
					<el-button @click="changeSelect();search()" slot="append" icon="el-icon-search"></el-button>
				</el-input>
			</div>
			<el-tabs v-model="message">
				<el-tab-pane :label="`未读新闻(${unread.length})`" name="first">
					<!-- 未读新闻列表 -->
					<el-table height="370px" :data="unread" :show-header="false" style="width: 100%">
						<el-table-column>
							<template slot-scope="scope">
								<el-button type="text"
									@click="get_row(scope.row.title,scope.row.content,scope.$index);show_dialog()">{{scope.row.title}}</el-button>
							</template>
						</el-table-column>
						<el-table-column>
							<template slot-scope="scope">
								<span class="message-author">{{scope.row.author}}</span>
							</template>
						</el-table-column>
						<el-table-column>
							<template slot-scope="scope">
								<span class="message-publishtime">{{scope.row.publishtime}}</span>
							</template>
						</el-table-column>
						<el-table-column width="120">
							<template slot-scope="scope">
								<el-button size="small" @click="handleRead(scope.$index)">标为已读</el-button>
							</template>
						</el-table-column>
					</el-table>
					<div class="login-btn">
						<el-button type="success" @click="getData()">刷新获取数据</el-button>
					</div>
				</el-tab-pane>
				<el-tab-pane :label="`阅读历史(${read.length})`" name="second">
					<template v-if="message === 'second'">
						<!-- 阅读历史列表 -->
						<el-table :data="read" :show-header="false" style="width: 100%">
							<el-table-column>
								<template slot-scope="scope">
									<el-button type="text"
										@click="get_row(scope.row.title,scope.row.content,scope.$index);show_dialog()">{{scope.row.title}}</el-button>
								</template>
							</el-table-column>
							<el-table-column prop="publishtime" width="150"></el-table-column>
						</el-table>
					</template>
				</el-tab-pane>
			</el-tabs>
		</div>
		<!-- 新闻详情对话框 -->
		<el-dialog :show-close="false" :title="temp_title" :visible.sync="dialogVisible" width="50%">
			<span>{{temp_content}}</span>
			<span slot="footer" class="dialog-footer">
				<el-button type="success" @click="dialogVisible = false;set_null()">确定</el-button>
			</span>
		</el-dialog>
	</div>
</template>

<script>
	import {
		r_ReturnNews
	} from '../../api/index.js'
	import {
		getnews
	} from '../../api/index.js'

	export default {
		name: 'tabs',
		data: function() {
			return {
				dialogVisible: false,
				message: 'first',
				showHeader: false,
				input: '',
				select: '',
				search_params: {
					input: '',
					select: ''
				},
				unread: [{
					publishtime: null,
					title: null,
					author: null,
					content: null
				}],
				read: [{
					publishtime: '',
					title: '',
					author: '',
					content: ''
				}],
				temp_content: '',
				temp_title: '',
				row_index: ''
			}
		},
		created() {
			this.getData();
			// 定时刷新数据
			setInterval(this.getData, 600000);
		},
		methods: {
			
			// 清空对话框内容和索引
			set_null() {
				this.temp_content = '';
				this.temp_title = '';
				this.row_index = '';
			},
			// 获取点击的行的内容和索引
			get_row(title, content, index) {
				this.temp_content = content;
				this.temp_title = title;
				this.row_index = index;
			},
			// 显示新闻详情对话框
			show_dialog() {
				this.dialogVisible = true;
			},
			// 更新搜索参数
			changeSelect() {
				this.$set(this.search_params, 'select', this.select);
				this.$set(this.search_params, 'input', this.input);
			},
			// 获取数据
			getData() {
				r_ReturnNews().then(res => {
					this.unread = res.ReturnResult;
				});
			},
			// 搜索新闻
			search() {
				console.log(this.search_params);
				if (this.input == 0 && this.select == 0) {
					this.$message.error('搜索不能为空ヽ(`Д´)ﾉ');
				} else if (this.input != 0 && this.select == 0) {
					this.$message.error('请选择搜索类别ヽ(`Д´)ﾉ');
				} else if (this.input == 0 && this.select != 0) {
					this.getData();
				} else {
					getnews(this.search_params).then(s_res => {
						console.log(s_res);
						if (s_res.code == 200) {
							this.unread = s_res.SearchResult;
						} else {
							this.$message.error('搜索不到该新闻╮(╯﹏╰）╭');
							return false;
						}
					});
				}
			},
			// 将新闻标记为已读
			handleRead(index) {
				const item = this.unread.splice(index, 1);
				this.read = item.concat(this.read);
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

	.el-select .el-input {
		width: 90px;
	}

	.input-with-select .el-input-group__prepend {
		background-color: #fff;
	}
</style>