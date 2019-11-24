<template>

</template>

<script>
    import axios from 'axios'

    document.addEventListener('DOMContentLoaded', () => {
        document.querySelectorAll('select').forEach((select) => {
            select.selectedIndex = -1;
        });
    });

    function getProduct(id, callback) {
        axios({
            method: 'get',
            url: `/api/product/${id}`,
        }).then(resp => {
            callback(null, resp.data);
        }).catch(err => {
            callback(err, null);
        });
    }

    export default {
        name: "EditProduct",
        data() {
            return {
                chatbots: [],
                chatbot: null,
                rules: [],
                message_text: "",
                buttons: [],
                question: "",
                message_type: null,
                button_id: null,
                all_buttons: [],
            }
        },
        mounted() {
            this.getProducts();
        },
        beforeRouteEnter(to, from, next) {
            getProduct(to.params.id, (err, data) => {
                next(vm => vm.setData(err, data));
            });
        },
        beforeRouteUpdate(to, from, next) {
            this.chatbot = null;
            getProduct(to.params.id, (err, data) => {
                this.setData(err, data);
                next();
            })
        },
        methods: {
            setData(err, product) {
                if (err) {
                    console.error(err);
                } else {
                    this.product = product
                }
            },
            getProducts() {
                axios({
                    method: 'get',
                    url: '/api/products/',
                }).then(resp => {
                    this.chatbots = resp.data.results;
                });
            }
        }
    }
</script>

<style scoped>

</style>
