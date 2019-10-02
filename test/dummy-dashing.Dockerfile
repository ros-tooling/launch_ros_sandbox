FROM osrf/ros:dashing-desktop

RUN touch dummy
ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]
