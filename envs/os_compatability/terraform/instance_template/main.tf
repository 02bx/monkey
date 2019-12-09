resource "aws_instance" "os_test_machine" {
  ami           = "${var.ami}"
  instance_type = "t2.micro"
  private_ip = "${var.ip}"
  subnet_id = "${data.aws_subnet.main.id}"
  key_name = "os_compat"
  tags = {
    Name = "${var.name}"
  }
  security_groups = ["${data.aws_security_group.os_compat_instance.id}"]
  associate_public_ip_address = false
}
