京东商品分类页面无法得到商品的价格和评价数，只能得到商品的名称和商品的唯一标识符（sku），
通过“https://p.3.cn/prices/mgets?skuIds=J_” + sku 得到商品的价格，
通过“https://club.jd.com/comment/productCommentSummaries.action?referenceIds=” + sku得到商品的评论数
每个商品的详情页url为 “https://item.jd.com/” + sku + “.html”
由于详情页面的爬取比较慢，所以最后再进行爬取，使用一个“lin”文件记录爬取进度，方便断点续爬

manmanbuy 平台会封ip，爬取历史价格的接口为“http://tool.manmanbuy.com/history.aspx?DA=1&action=gethistory&url=http%253A%2F%2Fitem.jd.com%2F'+ sku +'.html&bjid=&spbh=&cxid=&zkid=&w=951&token=”+Token
Token由js动态生成，直接使用execjs 调用生成Token的js代码，拼接url
通过代理ip爬取历史价格

爬取结果分为:
egg.csv：商品sku，名称，评论数，价格和详情页面url
des.csv：商品的sku和详情页面的详细信息
history.csv：商品的sku和manmanbuy平台上商品的历史价格
最后再拼接为：
last.csv