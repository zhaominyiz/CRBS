<template>
    <div>
        <Row>
            <Col>
                <Table :context="vm" :columns="columns" :data="tasks">
                </Table>
            </Col>
        </Row>    
        <div style="margin: 10px;overflow: visible">
            <div style="float: right;">
                <Page :total="cnt" :page-size="pageSize"
                 show-sizer :current="1" :page-size-opts="[5, 10]"
                  @on-change="changePage" @on-page-size-change="changePageSize"></Page>
            </div>
        </div>
    </div>
</template>

<script>
const listTask = {
    data () {
        const data = {
            vm: this,
            cnt: 0,
            pageSize: 10,
            currentPage: 1,
            columns: [
                {
                  title:"文件名",
                  key:'filename'
                },
                {
                    title: "语言",
                    key: 'language',
                },
                {
                    title: "简介",
                    key: 'caption',
                    render (h, {row, column, index}) {
                        // return `<Poptip placement="bottom" trigger="hover">
                        // <div slot="title"><i>Description</i></div>
                        // <p style="color: #00cc66" slot="content">${row.description}</p>
                        // ${row.caption}
                        // </Poptip>`

                        return h('Poptip',{
                            placement: 'bottom',
                            trigger: 'hover'
                        }, [
                            h('div', {
                                props: {
                                    slot: 'title'
                                }
                            }, [
                                h('i', {}, ['Description'])
                            ]),
                            h('p', {
                                style: {
                                    color: '#00cc66'
                                },
                                props: {
                                    slot: 'content'
                                }
                            }, [row.description]),
                            row.caption
                        ])
                    }
                },
                {
                    title: "创建时间",
                    key: "time",
                },
                {
                    title: "状态",
                    key: "status",
                },
                {
                    title: "操作",
                    key: "id",
                    render (h, {row, column, index}) {
                        // return `<i-button type="primary" size="small" @click="show(${row.id})">查看结果</i-button> `;
                        return h('i-button', {
                            props: {
                                type: 'primary',
                                size: 'small'
                            },
                            on: {
                                click: () => {
                                    data.vm.show(row.id)
                                }
                            }
                        }, ['查看结果'])
                    }
                }
            ],
            tasks: [
            ]
        }

        return data;
    },
    mounted(){
      var data = {
                userName:sessionStorage.getItem('username'),
                page:1,
                pageSize : 10,
      }
      console.log(data)
      this.$http.post('api/getqueue',data).then(
        (Response) => {
          this.tasks = Response.body.list
          this.currentPage = 1
        }
      )
    },
    computed: {
        pages () {
            return Math.ceil(this.cnt / this.pageSize)
        }
    },
    methods: {
        show (id) {
            console.log('show', id)
            sessionStorage.setItem("taskid",id)
            this.$router.push({
                path: '../detail',
                // query: {
                //     taskid: id
                // }
            })
        },
        changePage (page) {
            var data = {
                page: page,
                pageSize: this.pageSize,
            }
            this.$http.get('api/tasks', {
                params: data
            }).then(
                (Response) => {
                    this.tasks = Response.body.tasks
                    this.currentPage = page

                }
            )
        },
        changePageSize (pageSize) {
            var data = {
                page: 1,
                pageSize: pageSize,
            }
            this.$http.get('api/tasks', {
                params: data
            }).then(
                (Response) => {
                    this.tasks = Response.body.tasks
                    this.pageSize = pageSize
                }
            )
        },
    },
    // mounted () {
    //   alert("???")
    //     // next(vm => {
    //     //     // vm.$http.get('api/tasks/count').then(
    //     //     //     (Response) => {
    //     //     //         vm.cnt = Response.body.count
    //     //     //         var data = {
    //     //     //             page: vm.currentPage,
    //     //     //             pageSize: vm.pageSize,
    //     //     //         }
    //     //     //         vm.$http.get('api/tasks', {
    //     //     //             params: data
    //     //     //         }).then(
    //     //     //             (Response) => {
    //     //     //                 vm.tasks = Response.body.tasks
    //     //     //             }
    //     //     //         )
    //     //     //     }
    //     //     // )
    //     //             var data = {
    //     //                 userName:sessionStorage.getItem('username')
    //     //             }
    //     //             this.$http.get('api/getqueue', {
    //     //                 params: data
    //     //             }).then(
    //     //                 (Response) => {
    //     //                     this.tasks = Response.body.list
    //     //                 }
    //     //             )
    //     // })
    // }
}

export default listTask
</script>
