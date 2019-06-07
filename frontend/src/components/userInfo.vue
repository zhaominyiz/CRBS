<template>
    <div>
        <Form :model="form" :label-width="80">
            <Form-item label="用户名">
                <Input v-model="form.username" disabled="disabled" placeholder="请输入"></Input>
            </Form-item>
            <Form-item label="姓名">
                <Input v-model="form.name" placeholder="请输入姓名"></Input>
            </Form-item>
            <Form-item label="Email">
                <Input v-model="form.email" placeholder="请输入"></Input>
            </Form-item>
            <Form-item label="注册时间">
                <Date-picker :readonly="true" type="datetime" v-model="form.date_joined" placeholder="选择日期和时间" style="width: 200px"></Date-picker>
            </Form-item>
            <Form-item label="原密码">
                <Input type="password" v-model="form.rawPassword" placeholder="请输入原始密码"></Input>
            </Form-item>
            <Form-item label="新密码">
                <Input type="password" v-model="form.newPassword" placeholder="留空则不修改"></Input>
            </Form-item>
            <Form-item>
                <Button type="primary" @click="update">修改</Button>
            </Form-item>
        </Form>
    </div>
</template>

<script>
    export default {
    data () {
        return {
            form: {
                username: "",
                name: "",
                email: "",
                date_joined: null,
                rawPassword: "",
                newPassword: "",
            }
        }
    },
    computed: {
    },
    methods: {
        update: function () {
            this.$http.put('api/users/current', this.form).then(
                (Response) => {
                    this.$Notice.open({
                        'title': Response.body
                    })
                },
                (Response) => {
                    if (Response.status == 401)
                        return
                    this.$Notice.error({
                        'title': Response.body
                    })
                }
            )
        },
    },
    beforeRouteEnter (to, from , next) {
        next(vm => {
            var url = 'api/users/current'
            vm.$http.get(url).then(
                (Response) => {
                    var body = Response.body
                    vm.form.username = body.username
                    vm.form.name = body.name
                    vm.form.email = body.email
                    vm.form.date_joined = body.date_joined
                }
            )
        })
    },
    components: {
    }
}
</script>
<style scope>
    .code {
        max-height: 500px;
        overflow: scroll;
    }
</style>