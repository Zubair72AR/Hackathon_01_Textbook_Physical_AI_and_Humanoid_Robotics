import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useBaseUrl from '@docusaurus/useBaseUrl';
import styles from './BookNavigation.module.css';

function BookNavigation() {
  return (
    <div className={styles.bookNavigation}>
      <h3>Book Navigation</h3>
      <ul className={styles.navList}>
        <li><Link to="/docs/intro">Introduction</Link></li>
        <li>
          <Link to="/docs/module1-robotic-nervous-system">
            Module 1: Robotic Nervous System (ROS 2)
          </Link>
          <ul>
            <li>
              <Link to="/docs/module1-robotic-nervous-system/chapter1-ros2-fundamentals/nodes-topics-services">
                Chapter 1: ROS 2 Fundamentals
              </Link>
            </li>
          </ul>
        </li>
      </ul>
    </div>
  );
}

export default BookNavigation;