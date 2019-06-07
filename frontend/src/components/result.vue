<template>
    <div>
        <Table :context="vm" :columns="columns" :data="pairs"
        @on-row-click="clickRow">
        </Table>
        <div style="margin: 10px;overflow: visible">
            <div style="float: right;">
                <Page :total="cnt" :page-size="pageSize"
                 show-sizer show-elevator :current="1" :page-size-opts="[10, 20]"
                  @on-change="changePage" @on-page-size-change="changePageSize"></Page>
            </div>
        </div>
        <Modal ref="modal" v-model="showPair" :scrollable="true"
         :styles="{top: '20px', max: '20px'}" :width="1000"
         >
            <Row :gutter="32">
                <Col span="12">
                    <Card >
                        <p slot="title">{{srcName}}</p>
                        <code-fragment ref="cfSrc" :code="srcCode" :fragments="srcFragments"></code-fragment>
                    </Card>
                </Col>
                <Col span="12">
                    <Card >
                        <p slot="title">{{dstName}}</p>
                        <code-fragment ref="cfDst" :code="dstCode" :fragments="dstFragments"></code-fragment>
                    </Card>
                </Col>
            </Row>
        </Modal>
    </div>
</template>

<script>
    import Vue from 'vue';
    export default {
    data () {
        return {
            showPair: false,
            vm: this,
            cnt: 0,
            pageSize: 10,
            currentPage: 1,
            columns: [
                {
                    title: "源代码",
                    key: 'src',
                },
                {
                    title: "目的代码",
                    key: 'dst',
                },
                {
                    title: "相似度",
                    key: 'similarity'
                }
            ],
            pairs: [

            ],
            srcCode: "",
            dstCode: "",
            srcFragments: [[0, 0]],
            dstFragments: [[0, 0]],
            srcName: "",
            dstName: "",
        }
    },
    computed: {
    },
    methods: {
        changePage (page) {
            var url = `api/tasks/${this.$route.query.taskid}/results`
            this.currentPage = page
            var data = {
                page: this.currentPage,
                pageSize: this.pageSize,
            }
            this.$http.get(url, {
                params: data
            }).then(
                (Response) => {
                    this.pairs = Response.body.results
                }
            )
        },
        changePageSize (pageSize) {
            var url = `api/tasks/${this.$route.query.taskid}/results`
            this.pageSize = pageSize
            var data = {
                page: this.currentPage,
                pageSize: this.pageSize,
            }
            this.$http.get(url, {
                params: data
            }).then(
                (Response) => {
                    this.pairs = Response.body.results
                }
            )
        },
        clickRow (row) {
            this.$http.get(`api/results/${row.id}`).then(
                (Response) => {
                    let pairs = Response.body.pairs
                    let srcFragments = pairs.map( (x) => x[0])
                    let dstFragments = pairs.map( (x) => x[1])
                    let srcCode = Response.body.srcCode
                    let dstCode = Response.body.dstCode
                    this.srcCode = srcCode
                    this.dstCode = dstCode
                    this.srcName = row.src
                    this.dstName = row.dst
                    this.srcFragments = srcFragments
                    this.dstFragments = dstFragments
                    this.showPair = true
                }
            )
        }
    },
    beforeRouteEnter (to, from , next) {
        next(vm => {
            var url = `api/tasks/${vm.$route.query.taskid}/results`
            var data = {
                page: vm.currentPage,
                pageSize: vm.pageSize,
            }
            vm.$http.get(url, {
                params: data
            }).then(
                (Response) => {
                    vm.pairs = Response.body.results
                }
            )
            var cntUrl = `api/tasks/${vm.$route.query.taskid}/results/count`
            vm.$http.get(cntUrl).then(
                (Response) => {
                    vm.cnt = Response.body.count
                }
            )
            // 下面这段代码在注册事件
            let cfSrc = vm.$refs.cfSrc
            let cfDst = vm.$refs.cfDst
            cfSrc.$on('scroll', (id) => {
                let preId = `${cfSrc.prefix}-${id}`
                document.getElementById(preId).scrollIntoView()
            })
            cfDst.$on('scroll', (id) => {
                let preId = `${cfDst.prefix}-${id}`
                document.getElementById(preId).scrollIntoView()
            })
            // Vue.set 不可以把一个value作为vue instance, 这里是在偷懒
            // 正确点的姿势应该是记录字符串. 在上层做映射
            // 或者使用bus
            cfSrc.other = cfDst
            cfDst.other = cfSrc
        })
    },
    components: {
        'code-fragment': require('./codeFragment.vue')
    }
}
</script>
<style scope>
    .code {
        max-height: 500px;
        overflow: scroll;
    }
</style>