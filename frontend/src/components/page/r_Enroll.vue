<template>
	<div class="enroll-ce">
		<div class="ms-enroll">
			<div class="ms-title">注册</div>
			<el-form :model="enroll_data" :rules="enroll_rules" ref="enroll_form" label-width="0px" class="ms-content">
				<!--昵称-->
				<el-form-item prop="username">
					<el-input v-model="enroll_data.username" placeholder="username">
						<el-button slot="prepend" icon="el-icon-lx-people"></el-button>
					</el-input>
				</el-form-item>
				<!--账号-->
				<el-form-item prop="userid">
					<el-input v-model="enroll_data.userid" placeholder="userid">
						<el-button slot="prepend" icon="el-icon-lx-people"></el-button>
					</el-input>
				</el-form-item>
				<!--输入密码-->
				<el-form-item prop="password">
					<el-input type="password" placeholder="password" v-model="enroll_data.password">
						<el-button slot="prepend" icon="el-icon-lx-lock"></el-button>
					</el-input>
				</el-form-item>
				<!--再次输入密码-->
				<el-form-item prop="rpassword">
					<el-input type="password" v-model="enroll_data.rpassword" placeholder="rpassword">
						<el-button slot="prepend" icon="el-icon-lx-lock"></el-button>
					</el-input>
				</el-form-item>
				<div class="enroll-btn">
					<el-button type="success" @click="submitForm()">确定注册</el-button>
				</div>
				<p class="enroll-tips"></p>
			</el-form>
		</div>
	</div>
</template>

<script>
	import {
		enrollInfo
	} from '../../api/index.js'
	export default {
		data: function() {
			return {
				enroll_data: {
					username: "",
					password: "",
					userid: "",

				},
				enroll_data2: {
					rpassword: "",
				},
				enroll_rules: {
					userid: [{
						required: true,
						min: 2,
						max: 16,
						message: '请输入账号',
						trigger: 'blur'
					}],
					username: [{
						required: true,
						min: 2,
						max: 16,
						message: '请输入昵称',
						trigger: 'blur'
					}],
					password: [{
						required: true,
						min: 6,
						max: 16,
						message: '请输入密码',
						trigger: 'blur'
					}],
					rpassword: [{
						required: true,
						min: 6,
						max: 16,
						message: '请再次输入密码',
						trigger: 'blur'
					}],
				},
			};
		},
		methods: {
			submitForm() {
				this.$refs.enroll_form.validate(valid => {
					if (valid) {
						//	console.log(res.code);
						if (this.enroll_data.rpassword == this.enroll_data.password) {
							enrollInfo(this.enroll_data).then(res => {
								//将注册接口得到的数据打印在控制台
								console.log(res.code);
								//检查是否有已被注册的用户账号重复
								if (res.code == 200) {
									this.$router.push('/r_usermanagement');
								};
								if (res.code == "sameuserid") {
									this.$message.error('该账号已被注册过，请使用其他账号');
									console.log('sameid');
									return false;
								}
								//this.$router.push('/r_login');
							});
						} else {
							this.$message.error('请输入两次一致的密码');
							console.log('error rpassword');
							return false;
						}
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
	.enroll-ce {
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

	.ms-enroll {
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

	.enroll-btn {
		text-align: center;
	}

	.enroll-btn button {
		width: 100%;
		height: 36px;
		margin-bottom: 10px;
	}

	.enroll-tips {
		font-size: 12px;
		line-height: 30px;
		color: #fff;
	}
</style>