import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router);

export default new Router({
	routes: [{
			path: '/',
			redirect: '/r_login'
		},
		{
			path: '/',
			component: () => import( /* webpackChunkName: "home" */ '../components/common/Home.vue'),
			meta: {
				title: '自述文件'
			},
			children: [
					{//修改为环境表格页面
					path: '/r_evopage',
					component: () => import( /* webpackChunkName: "dashboard" */
						'../components/page/r_EvoPage.vue'),
					meta: {
						title: '历史数据'
					}
				},
				{
					path: '/r_usermanagement',
					component: () => import( /* webpackChunkName: "tabs" */
						'../components/page/r_UserManagement.vue'),
					meta: {
						title: '用户管理'
					}
				},
				{
					path: '/r_tabs',
					component: () => import( /* webpackChunkName: "tabs" */
						'../components/page/r_Tabs.vue'),
					meta: {
						title: '新闻视界'
					}
				},
				{
					// vue-schart组件
					path: '/r_charts',
					component: () => import( /* webpackChunkName: "chart" */
						'../components/page/r_Charts.vue'),
					meta: {
						title: '温度图表'
					}
				},
				{
					// vue-schart组件
					path: '/r_charts1',
					component: () => import( /* webpackChunkName: "chart" */
						'../components/page/r_Charts1.vue'),
					meta: {
						title: '光照图表'
					}
				},
				{
					// vue-schart组件
					path: '/r_charts2',
					component: () => import( /* webpackChunkName: "chart" */
						'../components/page/r_Charts2.vue'),
					meta: {
						title: '湿度图表'
					}
				},
				{
					// vue-schart组件
					path: '/r_advise',
					component: () => import( /* webpackChunkName: "chart" */
						'../components/page/r_Advise.vue'),
					meta: {
						title: '专家建议'
					}
				},
				{
					path: '/404',
					component: () => import( /* webpackChunkName: "404" */
						'../components/page/404.vue'),
					meta: {
						title: '404'
					}
				},
				{
					path: '/403',
					component: () => import( /* webpackChunkName: "403" */
						'../components/page/403.vue'),
					meta: {
						title: '403'
					}
				},
				
			]
		},
		{
			path: '/enroll',
			component: () => import( /* webpackChunkName: "r_login" */ '../components/page/r_Enroll.vue'),
			meta: {
				title: '注册'
			}
		},
		{
			path: '/r_login',
			component: () => import( /* webpackChunkName: "r_login" */ '../components/page/r_Login.vue'),
			meta: {
				title: '登录'
			}
		},
		{
			path: '*',
			redirect: '/r_login'
		}
	]
});