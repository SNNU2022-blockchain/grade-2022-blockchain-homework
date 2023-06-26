// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LogisticsContract {
    address public supplier;
    address public  transporter;

    uint256 public orderAmount;
    uint256 public transportFee;
    uint256 public key;//密钥
    bool public orderPlaced;
    bool public feePaid;
    bool public complete;
    bool public confirm_complete;
    string public place1;
    string public place2;
    string public place3;

    uint256 public releaseTime;
    
    event OrderPlaced(address indexed supplier, uint256 amount);
    event TransportFeePaid(address indexed transporter, uint256 fee);
    //参数为开放时间
    constructor(uint256 _releaseTime) {
        supplier = msg.sender;
        orderPlaced = false;
        feePaid = false;
        releaseTime=_releaseTime;
    }
    //自定义修饰符
    modifier onlySupplier() {
        require(msg.sender == supplier, "Only supplier can perform this action");
        _;
    }

    modifier onlyTransporter() {
        require(msg.sender == transporter, "Only transporter can perform this action");
        _;
    }
    //供应商下单，同时提供key
    function placeOrder(uint _key) payable public  {
        require(!orderPlaced, "Order has already been placed");
        payable(address(this)).transfer(msg.value);
        orderAmount = msg.value;
        orderPlaced = true;
        key=_key;
    }

     // 获取合约账户余额 
    function getBalanceOfContract() public view returns (uint256) {
        return address(this).balance;
    }


    function setTransporter(address _transporter) public onlySupplier {
        require(orderPlaced, "Order has already been placed");
        transporter = _transporter;
        
    }
    //运输跟踪
    function updatePlace1(string memory _place) public onlyTransporter {
        place1 = _place;
    }

    function updatePlace2(string memory _place) public onlyTransporter {
        place2 = _place;
    }

    function updatePlace3(string memory _place) public onlyTransporter {
        place3 = _place;
    }
    //运输方与供应商都确认才可支付运费
    function completeDelivery() public onlyTransporter {
        complete=true;
    }
    function confirm_receipt() public onlySupplier {
        confirm_complete=true;
    }
    // function withdrawAll(address payable transporter) public {
    //     transporter.transfer(address(this).balance);
    // }
    function payTransFee(address payable addr,uint _key)public payable onlyTransporter{
        //输入地址，给运输方地址转账运费
        require(confirm_complete, "Order has not been placed yet");
        require(_key==key, "Order has not been placed yet");
        addr.transfer(address(this).balance);
    }
    //时间锁，防止订单失效钱无法取出
    function withdraw(address payable beneficiary) external {
        require(block.timestamp >= releaseTime, "Time lock not expired yet");
        beneficiary.transfer(address(this).balance);
    }
    fallback() external payable {}
    receive() external payable {}
}
