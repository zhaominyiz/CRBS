<template>
    <div>
        <Row>
            <Col>
                <Breadcrumb>
                    <Breadcrumb-item href="/history/">任务记录</Breadcrumb-item>
                    <Breadcrumb-item v-if=" $route.path=='/history/detial' " href="/history/detial">查重结果</Breadcrumb-item>
                </Breadcrumb>
            </Col>
        </Row>
        <br/>
        <Row>
            <Col>
                <router-view></router-view>
            </Col>
        </Row>
    </div>
</template>

<script>
    export default {
    data () {
        return {
        }
    },
    computed: {
    },
    methods: {
    }
}
</script>
