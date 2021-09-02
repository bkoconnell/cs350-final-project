const index = (req, res) => {
    res.render('index', {title: "DHT Dashboard"});
};

module.exports = {
    index
}