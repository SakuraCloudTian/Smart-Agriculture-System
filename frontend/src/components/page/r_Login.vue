<template>
	<div class="login-ce">
		<div class="ms-login">
			<div class="ms-title">登录</div>
			<!-- 登录表单 -->
			<el-form :model="login_data" :rules="login_rules" ref="login_form" label-width="0px" class="ms-content">
				<!-- 用户名 -->
				<el-form-item prop="userid">
					<el-input v-model="login_data.userid" placeholder="userid">
						<el-button slot="prepend" icon="el-icon-lx-people"></el-button>
					</el-input>
				</el-form-item>
				<!-- 密码 -->
				<el-form-item prop="password">
					<el-input type="password" placeholder="password" v-model="login_data.password"
						@keyup.enter.native="submitForm()">
						<el-button slot="prepend" icon="el-icon-lx-lock"></el-button>
					</el-input>
				</el-form-item>
				<div class="login-btn">
					<!-- 登录按钮 -->
					<el-button type="success" @click="submitForm()">登录</el-button>
				</div>
				<!-- 注册按钮 -->
				<el-button type="text" @click="enroll()">注册</el-button>
				<p class="login-tips"></p>
			</el-form>
		</div>
	</div>
</template>

<script>
	// 导入登录账号的API函数
	import {
		r_LoginInfo
	} from '../../api/index.js';

	export default {
		data: function() {
			return {
				login_data: {
					userid: "",
					password: "",
				},
				login_rules: {
					userid: [{
						required: true,
						min: 2,
						max: 16,
						message: '请输入用户名',
						trigger: 'blur'
					}],
					password: [{
						required: true,
						min: 6,
						max: 12,
						message: '请输入密码',
						trigger: 'blur'
					}],
				},
			};
		},
		methods: {
			// 注册按钮点击事件
			enroll() {
				localStorage.setItem('ms_username', "admin");
				this.$router.push('/enroll');
			},
			// 表单提交
			submitForm() {
				this.$refs.login_form.validate(valid => {
					if (valid) {
						// 验证通过
						r_LoginInfo(this.login_data).then(res => {
							// 将登录接口得到的数据打印在控制台
							console.log(res.code);
							if (res.code == 200) {
								
								localStorage.setItem('ms_username', res.loginInfo[0].username);
								localStorage.setItem('ms_userid', res.loginInfo[0].userid);
								this.$router.push('/r_evopage');
								this.$message.success('登录成功');
							} else {
								this.$message.error('账号或密码错误!!!');
								console.log('wrong userid or password!!');
								return false;
							}
						});
					} else {
						this.$message.error('请输入账号和密码');
						console.log('error submit!!');
						return false;
					}
				});
				
			},
		},
	};
</script>

<style scoped>
	.login-ce {
		position: relative;
		width: 100%;
		height: 100%;
		background-image: url(../../assets/img/BackgroundImg.jpg);
		
		background-size: 100%;
	}

	.ms-title {
		width: 100%;
		line-height: 50px;
		text-align: center;
		font-size: 20px;
		color: #fff;
		border-bottom: 1px solid #ddd;
	}

	.ms-login {
		position: absolute;
		left: 50%;
		top: 50%;
		width: 350px;
		margin: -190px 0 0 -175px;
		border-radius: 5px;
		background: rgba(255, 255, 255, 0.3);
		overflow: hidden;
	}

	.ms-content {
		padding: 30px 30px;
	}

	.login-btn {
		text-align: center;
	}

	.login-btn button {
		width: 100%;
		height: 36px;
		margin-bottom: 10px;
	}

	.login-tips {
		font-size: 12px;
		line-height: 30px;
		color: #fff;
	}
</style>